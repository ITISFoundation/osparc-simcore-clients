# NOTES

For the moment, we have to apply some changes manually until we use [templates](https://openapi-generator.tech/docs/templating) or [customization](https://openapi-generator.tech/docs/customization)

### Workflow

- update OAS -> ``api/openapi.json``
- generate client ``make python-client``
- generate documentation ``make postprocess-docs``


----

# @channel :tada:  Released new ``osparc==0.5.0`` python client library

## Highlights:

- ✨ adds ``SolverApi.get_job_output_logfile`` to download logfile after a job run (#27)
- Checkout updated [doc](https://itisfoundation.github.io/osparc-simcore-clients) and [tutorial](https://itisfoundation.github.io/osparc-simcore-clients/#/md/tutorials/BasicTutorial?id=basic-tutorial)
- Do you to want to report a bug, have a request or a question about ``osparc`` library? Drop it [in our issue tracker](https://github.com/ITISFoundation/osparc-simcore-clients/issues/new/choose)

## More details
- [Release Notes](https://github.com/ITISFoundation/osparc-simcore-clients/releases)
- [Documentation](https://itisfoundation.github.io/osparc-simcore-clients)
- [Repository](https://github.com/ITISFoundation/osparc-simcore-clients)
