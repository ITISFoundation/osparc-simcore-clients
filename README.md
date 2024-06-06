<h1 align="center">oSPARC-Simcore-Clients</h1>

To get started using the tools developed in this repository have a look at the
[Documentation](https://itisfoundation.github.io/osparc-simcore-clients).

For more in depth knowledge concerning the development of the repository, take a look at
- [Release Notes](https://github.com/ITISFoundation/osparc-simcore-clients/releases)
- [Development notes](#development-notes)

For reporting an issue, use our [issue tracker](https://github.com/ITISFoundation/osparc-simcore-clients/issues/new/choose)

# Development notes

These notes are intended for people who want to contribute to the development of this repository.

The different clients for the oSPARC public API are generated using the [openapi-generator](https://github.com/ITISFoundation/openapi-generator)-tool.
*The generated files should not be changed manually!*
Instead proposed changes should be implemented directly on the [openapi-generator](https://github.com/ITISFoundation/openapi-generator)-repository.
See also [templates](https://openapi-generator.tech/docs/templating) and [customization](https://openapi-generator.tech/docs/customization).

## Workflow

See the different `clients/<language>/README.md` for the workflows for generating the different clients. Here is the workflow which all clients have in common:

- To generate a client one needs two "ingredients":
    1. The openapi specification which is a json file located in `api/openapi.json`. This generated in [osparc-simcore](https://github.com/ITISFoundation/osparc-simcore/tree/master/services/api-server) and then moved here.
    2. The [openapi-generator](https://github.com/ITISFoundation/openapi-generator)-tool. The exact docker image of this tool to use is specifies in `scripts/common.Makefile`.

## Code lifecycle
This link explains the lifecycle of the osparc client(s) (borrowed from https://www.ibm.com/docs/en/acvfc?topic=manager-product-lifecycle)
<p align="center">
<a href="https://www.ibm.com/docs/en/acvfc?topic=manager-product-lifecycle" target="_blank">
<image src="https://github.com/ITISFoundation/osparc-simcore-clients/blob/master/docs/_media/code_lifecycle.png?raw=true" alt="Code lifecycle" width="50%" />
</a>
</p>


## Documentation

Each client (corresponding to a directory `clients/<language>`) should have a make recipy called `install-doc` which installs packages needed to generate the documentation for that client, as well as a make recipe `docs` which generates the documentation. All of these recipes are called from the root's `docs` recipe, which is what is called when the website is published.

# Repos which depend on this one

Here is an inexhaustive list which have this repo as a dependency. So changing stuff here might break stuff there:

- [e2e-portal-testing](https://git.speag.com/oSparc/e2e-portal-testing/-/commit/950762bde1a60c7ce23286da9c100150ed6926e4)
- [osparc-simcore](https://github.com/ITISFoundation/osparc-simcore/actions/runs/5319311892/jobs/9631979977)

<p align="center">
<a href="https://www.z43.swiss" target="_blank">
<image src="https://github.com/ITISFoundation/osparc-simcore-clients/blob/master/docs/_media/mwl.png?raw=true" alt="Made with love (and lots of hard work) at www.z43.swiss" width="20%" />
</a>
</p>
