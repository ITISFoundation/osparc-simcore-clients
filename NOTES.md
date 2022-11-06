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
    - remove generator entry (since some custom changes)
    - from '## Documentation for API Endpoints' to '## Author'
    - ``Documentation for API Classes`` instead of ``Documentation for API Endpoints``
          - ``Back to API list`` to ``Back to API Classes``
    - ``## Author`` also is different in md/README.md
  - remove ```# Defining host is optional and default to https://api.osparc.io
configuration.host = "https://api.osparc.io"```
  - Updates notebooks: ``make notebooks``
    - Apply fixes to ``BasicTutorial.ipynb``  as in https://github.com/ITISFoundation/osparc-simcore-python-client/pull/35



----

# @channel :tada:  Released new ``osparc==0.5.0`` python client library

## Highlights:

- ✨ adds ``SolverApi.get_job_output_logfile`` to download logfile after a job run (#27)
- Checkout updated [doc](https://itisfoundation.github.io/osparc-simcore-python-client) and [tutorial](https://itisfoundation.github.io/osparc-simcore-python-client/#/md/tutorials/BasicTutorial?id=basic-tutorial)
- Do you to want to report a bug, have a request or a question about ``osparc`` library? Drop it [in our issue tracker](https://github.com/ITISFoundation/osparc-simcore-python-client/issues/new/choose)

## More details
- [Release Notes](https://github.com/ITISFoundation/osparc-simcore-python-client/releases)
- [Documentation](https://itisfoundation.github.io/osparc-simcore-python-client)
- [Repository](https://github.com/ITISFoundation/osparc-simcore-python-client)
