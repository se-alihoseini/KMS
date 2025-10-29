#!/bin/bash

# ===============================
# API Creator Script for Django
# ===============================

# Ask for input
read -p "Enter app name: " APP_NAME
read -p "Enter API name (e.g. user_login): " API_NAME
read -p "Enter HTTP method (POST, GET, etc.): " API_METHOD

# Paths
APP_DIR="./$APP_NAME"
VALIDATOR_DIR="$APP_DIR/validators"
USECASE_DIR="$APP_DIR/usecase"
VIEWS_DIR="$APP_DIR/api/v1/views"
URLS_FILE="$APP_DIR/api/v1/urls.py"
INIT_FILE="$VIEWS_DIR/__init__.py"

# Convert API name to CamelCase for class names
API_CLASS_NAME="$(echo $API_NAME | sed -r 's/(^|_)([a-z])/\U\2/g')"

# -------------------------------
# 1. Create Validator
# -------------------------------
VALIDATOR_FILE="$VALIDATOR_DIR/${API_NAME}_validator.py"
if [ ! -f "$VALIDATOR_FILE" ]; then
cat <<EOL > "$VALIDATOR_FILE"
from pydantic import BaseModel

class ${API_CLASS_NAME}Validator(BaseModel):
    # TODO: add your fields
    pass
EOL
echo "✅ Validator created: $VALIDATOR_FILE"
else
echo "⚠ Validator already exists: $VALIDATOR_FILE"
fi

# -------------------------------
# 2. Create UseCase
# -------------------------------
USECASE_FILE="$USECASE_DIR/${API_NAME}_usecase.py"
if [ ! -f "$USECASE_FILE" ]; then
cat <<EOL > "$USECASE_FILE"
from backbone.interface import UseCaseInterface
from django.http import JsonResponse
from $APP_NAME.validators.${API_NAME}_validator import ${API_CLASS_NAME}Validator

class ${API_CLASS_NAME}UseCase(UseCaseInterface):
    def process_request(self, payload: ${API_CLASS_NAME}Validator):
        # TODO: implement your logic
        return JsonResponse({"success": True, "message": "API executed"}, status=200)
EOL
echo "✅ UseCase created: $USECASE_FILE"
else
echo "⚠ UseCase already exists: $USECASE_FILE"
fi

# -------------------------------
# 3. Create View
# -------------------------------
VIEW_FILE="$VIEWS_DIR/${API_NAME}.py"
if [ ! -f "$VIEW_FILE" ]; then
cat <<EOL > "$VIEW_FILE"
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse, HttpRequest
from $APP_NAME.usecase.${API_NAME}_usecase import ${API_CLASS_NAME}UseCase
from utils.general_functions.get_request_body import get_request_body
from $APP_NAME.validators.${API_NAME}_validator import ${API_CLASS_NAME}Validator

@require_http_methods(["$API_METHOD"])
def $API_NAME(request: HttpRequest) -> JsonResponse:
    payload = get_request_body(request=request, validator=${API_CLASS_NAME}Validator)
    use_case = ${API_CLASS_NAME}UseCase()
    data = use_case.execute(request_model=payload)
    return data
EOL
echo "✅ View created: $VIEW_FILE"
else
echo "⚠ View already exists: $VIEW_FILE"
fi

# -------------------------------
# 4. Add view import to __init__.py
# -------------------------------
if [ ! -f "$INIT_FILE" ]; then
    touch "$INIT_FILE"
fi

if ! grep -q "from .${API_NAME} import $API_NAME" "$INIT_FILE"; then
    echo "from .${API_NAME} import $API_NAME" >> "$INIT_FILE"
    echo "✅ Added import to __init__.py"
else
    echo "⚠ Import already exists in __init__.py"
fi

# -------------------------------
# 5. Add URL to urls.py
# -------------------------------
if ! grep -q "path(\"$API_NAME/" "$URLS_FILE"; then
    # Check if account_url_patterns exists
    if ! grep -q "account_url_patterns" "$URLS_FILE"; then
        echo -e "\naccount_url_patterns = []" >> "$URLS_FILE"
    fi
    # Add URL entry
    sed -i "/account_url_patterns = \[/ a \    path(\"$API_NAME/\", views.$API_NAME, name=\"$API_NAME\")," "$URLS_FILE"
    echo "✅ Added URL to $URLS_FILE"
else
    echo "⚠ URL already exists in $URLS_FILE"
fi

