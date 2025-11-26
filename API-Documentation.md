# CT4PWD Compiler API Documentation

## Overview

The CT4PWD Compiler API is a REST API that processes visual programming block images and compiles them into readable code output. It uses computer vision to detect QR codes representing programming constructs and validates the logic correctness.

**Base URL**: `http://localhost:5000` (replace with your server's URL)
**Version**: 1.0

---

## Endpoints

### 1. GET /

**Description**: API documentation and usage information

**Response**:

```json
{
  "message": "CT4PWD Compiler API",
  "version": "1.0",
  "endpoints": {
    "POST /compile": "Compile visual programming blocks from image",
    "GET /health": "Health check",
    "GET /": "API documentation"
  },
  "usage": {
    "compile": {
      "method": "POST",
      "endpoint": "/compile",
      "content_type": "application/json",
      "body": {
        "image_path": "string - path to the image file"
      },
      "example": {
        "image_path": "test-images/ifelse.png"
      }
    }
  }
}
```

---

### 2. GET /health

**Description**: Health check endpoint to verify API availability

**Response**:

```json
{
  "status": "healthy",
  "message": "CT4PWD Compiler API is running"
}
```

---

### 3. POST /compile

**Description**: Main compilation endpoint that processes visual programming block images

#### Request

- **Method**: `POST`
- **Content-Type**: `application/json`
- **Body**:
  ```json
  {
    "image_path": "string"
  }
  ```

#### Parameters

| Parameter  | Type   | Required | Description                                                                      |
| ---------- | ------ | -------- | -------------------------------------------------------------------------------- |
| image_path | string | Yes      | Relative or absolute path to the image file containing visual programming blocks |

#### Example Request

```json
{
  "image_path": "test-images/ifelse.png"
}
```

#### Response Format

```json
{
  "success": boolean,
  "is_correct": boolean,
  "output": string,
  "details": {
    "detected_blocks": array,
    "loop_count": number,
    "anchor_x": number,
    "parsed": object,
    "raw_output": string
  }
}
```

#### Response Fields

| Field                   | Type    | Description                                                          |
| ----------------------- | ------- | -------------------------------------------------------------------- |
| success                 | boolean | Indicates if the request was processed successfully                  |
| is_correct              | boolean | `true` if the visual programming logic is correct, `false` otherwise |
| output                  | string  | Clean compiled output or error message                               |
| details.detected_blocks | array   | Array of detected programming blocks from the image                  |
| details.loop_count      | number  | Number of loop iterations detected                                   |
| details.anchor_x        | number  | X-coordinate anchor point for block alignment                        |
| details.parsed          | object  | Parsed structure containing conditions, sequence, and colors         |
| details.raw_output      | string  | Raw output including correctness indicators                          |

#### Success Response Examples

**Correct Logic**:

```json
{
  "success": true,
  "is_correct": true,
  "output": "if red stop elseif green go",
  "details": {
    "detected_blocks": [
      { "type": "control", "value": "if" },
      { "type": "condition", "value": "red" },
      { "type": "action", "value": "stop" },
      { "type": "control", "value": "else" },
      { "type": "control", "value": "if" },
      { "type": "condition", "value": "green" },
      { "type": "action", "value": "go" }
    ],
    "loop_count": 1,
    "anchor_x": 1415,
    "parsed": {
      "colors": [],
      "conditions": [
        { "if": "red", "action": "stop" },
        { "elseif": "green", "action": "go" }
      ],
      "loop_count": 1,
      "sequence": ["if", "red", "stop", "elseif", "green", "go"]
    },
    "raw_output": "✓ CORRECT: if red stop elseif green go"
  }
}
```

**Incorrect Logic**:

```json
{
  "success": true,
  "is_correct": false,
  "output": "incorrect logic: red-go\ncorrect: red-stop",
  "details": {
    "detected_blocks": [...],
    "loop_count": 1,
    "anchor_x": 1200,
    "parsed": {...},
    "raw_output": "incorrect logic: red-go\ncorrect: red-stop"
  }
}
```

#### Error Response Examples

**File Not Found**:

```json
{
  "success": false,
  "is_correct": false,
  "output": "Image file not found: invalid/path.png",
  "details": null
}
```

**Missing Parameters**:

```json
{
  "success": false,
  "is_correct": false,
  "output": "Missing image_path in request body",
  "details": null
}
```

**Processing Error**:

```json
{
  "success": false,
  "is_correct": false,
  "output": "Could not read image file: corrupted.png",
  "details": null
}
```

#### HTTP Status Codes

| Code | Description                                 |
| ---- | ------------------------------------------- |
| 200  | Success - Request processed successfully    |
| 400  | Bad Request - Missing or invalid parameters |
| 404  | Not Found - Image file not found            |
| 500  | Internal Server Error - Processing error    |

---

## Supported Visual Programming Constructs

### Control Structures

- **if**: Conditional statement
- **elseif**: Alternative condition
- **else**: Default condition
- **loop**: Repetition construct

### Conditions

- **red**: Traffic light red
- **green**: Traffic light green
- **raining**: Weather condition
- **sunny**: Weather condition
- **snowing**: Weather condition

### Actions

- **stop**: Stop action
- **go**: Go action
- **umbrella**: Take umbrella
- **sunglasses**: Wear sunglasses
- **coat**: Wear coat

### Valid Logic Mappings

```
raining → umbrella
sunny → sunglasses
snowing → coat
green → go
red → stop
```

---

## Usage Examples

### cURL

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"image_path": "test-images/ifelse.png"}' \
  http://localhost:5000/compile
```

### PowerShell

```powershell
$body = '{"image_path": "test-images/ifelse.png"}'
Invoke-RestMethod -Uri "http://localhost:5000/compile" -Method POST -ContentType "application/json" -Body $body
```

### JavaScript (fetch)

```javascript
fetch("http://localhost:5000/compile", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
  },
  body: JSON.stringify({
    image_path: "test-images/ifelse.png",
  }),
})
  .then((response) => response.json())
  .then((data) => {
    if (data.is_correct) {
      console.log("✓ CORRECT:", data.output);
    } else {
      console.log("✗ INCORRECT:", data.output);
    }
  });
```

### Python (requests)

```python
import requests

url = "http://localhost:5000/compile"
payload = {"image_path": "test-images/ifelse.png"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)
data = response.json()

if data['is_correct']:
    print(f"✓ CORRECT: {data['output']}")
else:
    print(f"✗ INCORRECT: {data['output']}")
```

---

## Error Handling

The API provides detailed error messages to help diagnose issues:

### Logic Errors

- **Incorrect mappings**: Shows both incorrect and correct logic
- **Wrong arrangement**: Indicates blocks are not in proper sequence
- **Unknown conditions/actions**: Reports unrecognized programming constructs

### File Errors

- **File not found**: Checks if image path exists
- **Unreadable file**: Validates image format and integrity
- **Missing parameters**: Ensures required fields are provided

### Processing Errors

- **QR detection failure**: Issues with computer vision processing
- **Parsing errors**: Problems with block structure analysis

---

## Image Requirements

### Supported Formats

- PNG (recommended)
- JPEG
- Other formats supported by OpenCV

### Image Quality

- Clear, well-lit images
- QR codes should be easily readable
- Minimum resolution: 640x480
- Programming blocks should be properly aligned

### File Location

- Images should be accessible from the server's working directory
- Use relative paths from the server root or absolute paths
- Ensure proper file permissions

---

## Rate Limiting

Currently, no rate limiting is implemented. For production use, consider implementing rate limiting based on your requirements.

---

## Security Considerations

- The API accepts file paths as input - ensure proper path validation in production
- Consider implementing authentication for production deployments
- Validate and sanitize all input parameters
- Use HTTPS in production environments

---

## Dependencies

- Flask: Web framework
- OpenCV: Computer vision processing
- PyTesseract: OCR capabilities
- Pyzbar: QR code reading
- NumPy: Numerical operations

---

## Deployment

The API runs on port 5000 by default. For production deployment:

1. Use a production WSGI server (e.g., Gunicorn)
2. Configure proper logging
3. Set up error monitoring
4. Implement health checks
5. Use environment variables for configuration
