import json
import boto3
import uuid
from decimal import Decimal

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("Notes")

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)

def lambda_handler(event, context):

    # ---------- GET NOTES ----------
    if event.get("body") is None:
        response = table.scan()
        items = response.get("Items", [])

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"notes": items}, cls=DecimalEncoder)
        }

    # ---------- BODY PRESENT (POST / UPDATE / DELETE) ----------
    data = json.loads(event["body"])
    action = data.get("action", "create")

    # ---------- CREATE ----------
    if action == "create":
        item = {
            "noteID": str(uuid.uuid4()),
            "title": data.get("title", ""),
            "content": data.get("content", "")
        }

        table.put_item(Item=item)

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": "Note created", "note": item})
        }

    # ---------- UPDATE ----------
    if action == "update":
        table.update_item(
            Key={"noteID": data["noteID"]},
            UpdateExpression="SET title = :t, content = :c",
            ExpressionAttributeValues={
                ":t": data.get("title", ""),
                ":c": data.get("content", "")
            }
        )

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": "Note updated"})
        }

    # ---------- DELETE ----------
    if action == "delete":
        table.delete_item(
            Key={"noteID": data["noteID"]}
        )

        return {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            "body": json.dumps({"message": "Note deleted"})
        }

    # ---------- INVALID ----------
    return {
        "statusCode": 400,
        "body": json.dumps({"error": "Invalid action"})
    }
