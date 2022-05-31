# NOTES

For the moment, we have to apply some changes manually until we use [templates](https://openapi-generator.tech/docs/templating) or [customization](https://openapi-generator.tech/docs/customization)

### Workflow

- update OAS -> ``api/openapi.json``
- generate client ``make python-client``
- Apply patches to the code (SEE ``PATCH ---`` marks in code)
- md doc files
  - format all md?
  - replace 'YOUR_USERNAME' by 'YOUR_API_KEY_HERE'
  - replace 'YOUR_PASSWORD' by 'YOUR_API_SECRET_HERE'
  - replace 'http://localhost' by 'https://api.osparc.io'
  - replace ``:\n`` -> ``:\n\n`` after titles. Otherwise it docsify fails to render it correctly
  - move all to docs/md
  - update README.md
    - from '## Documentation for API Endpoints' to '## Author'
    - ``## Author`` also is different in md/README.md
