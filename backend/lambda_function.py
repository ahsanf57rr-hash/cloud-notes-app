def lambda_handler(event, context):
    print("🚀 Backend deployed via CodePipeline - VERSION 2")

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
            "body": json.dumps({
                "backendStatus": "✅ Backend updated via CodePipeline",
                "version": "v2",
                "notes": items
            }, cls=DecimalEncoder)
        }
