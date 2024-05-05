import json
import boto3

# Initialize S3 client
s3 = boto3.client('s3')

# Constants
BUCKET_NAME = 'todolistlut'  # Replace with your S3 bucket name
FILE_NAME = 'todolist.json'  # Replace with your JSON file name in S3

# Function to retrieve todo list from S3
def get_todo_list():
    try:
        response = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_NAME)
        todo_list = json.loads(response['Body'].read().decode('utf-8'))
        return todo_list
    except Exception as e:
        print("Error getting todo list:", e)
        return []

# Function to save todo list to S3
def save_todo_list(todo_list):
    try:
        s3.put_object(Bucket=BUCKET_NAME, Key=FILE_NAME, Body=json.dumps(todo_list))
    except Exception as e:
        print("Error saving todo list:", e)


# Lambda handler for adding a todo item
def lambda_handler(event, context):
    try:
        todo_list=[]
        todo_item = json.loads(event['body'])
        # todo_item = json.dumps(todo_item)
        response = s3.get_object(Bucket=BUCKET_NAME, Key=FILE_NAME)
        todo_list = json.loads(response['Body'])
        print(todo_list)
        todo_list.append(todo_item)
        todo_list.append(todo_item)
        # todo_list.dumps(todo_item)
        save_todo_list(todo_list)
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Todo item added successfully'})
        }
    except Exception as e:
        print("Error:", e)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error'})
        }

# Lambda handler for reading the todo list
def read_todo(event, context):
    try:
        todo_list = get_todo_list()
        return {
            'statusCode': 200,
            'body': json.dumps(todo_list)
        }
    except Exception as e:
        print("Error:", e)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error'})
        }

# Lambda handler for updating a todo item
def update_todo(event, context):
    try:
        updated_todo_item = json.loads(event['body'])
        todo_list = get_todo_list()
        for i, todo_item in enumerate(todo_list):
            if todo_item['id'] == updated_todo_item['id']:
                todo_list[i] = updated_todo_item
                save_todo_list(todo_list)
                return {
                    'statusCode': 200,
                    'body': json.dumps({'message': 'Todo item updated successfully'})
                }
        return {
            'statusCode': 404,
            'body': json.dumps({'message': 'Todo item not found'})
        }
    except Exception as e:
        print("Error:", e)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error'})
        }

# Lambda handler for deleting a todo item
def delete_todo(event, context):
    try:
        todo_item_id = json.loads(event['body'])['id']
        todo_list = get_todo_list()
        updated_todo_list = [todo_item for todo_item in todo_list if todo_item['id'] != todo_item_id]
        save_todo_list(updated_todo_list)
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Todo item deleted successfully'})
        }
    except Exception as e:
        print("Error:", e)
        return {
            'statusCode': 500,
            'body': json.dumps({'message': 'Internal server error'})
        }
