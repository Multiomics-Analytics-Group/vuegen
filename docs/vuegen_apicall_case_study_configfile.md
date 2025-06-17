# APICall Component Configuration File

A [configuration file](https://github.com/Multiomics-Analytics-Group/vuegen/blob/main/docs/example_config_files/APIcall_example_config.yaml) for the API call component is provided below:

```yaml
report:
  title: APICall example
  description: An APICall example.
sections:
  - title: APICall test
    subsections:
      - title: JSONPlaceholder test
        components:
          - title: GET request
            component_type: apicall
            api_url: https://jsonplaceholder.typicode.com/todos/1
            method: GET
          - title: POST request
            component_type: apicall
            api_url: https://jsonplaceholder.typicode.com/todos
            method: POST
            request_body: |
              {
                  "userId": 1,
                  "title": "Go running",
                  "completed": false
              }
          - title: PUT request
            component_type: apicall
            api_url: https://jsonplaceholder.typicode.com/todos/10
            method: PUT
            request_body: |
              {
                  "userId": 1,
                  "title": "Play the guitar",
                  "completed": true
              }
          - title: PATCH request
            component_type: apicall
            api_url: https://jsonplaceholder.typicode.com/todos/10
            method: PATCH
            request_body: |
              {
                  "title": "Go for a hike"
              }
          - title: DELETE request
            component_type: apicall
            api_url: https://jsonplaceholder.typicode.com/todos/10
            method: DELETE
```