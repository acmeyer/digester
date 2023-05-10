Given a document from a user, try to extract the following metadata:
- title: string
- description: string
- author: string
- created_at: string
Respond with a JSON containing the extracted metadata in key value pairs. If you don't find a metadata field, return an empty string for its value.