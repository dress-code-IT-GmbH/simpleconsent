# Simple Consent for Attribute Release

Web Service including GUI to obtain, store and maintain user consent
- Consent is all or nothing (no attribute selection)
- Can store consent for multiple relying parties
- Plug & play integration for SATOSA
- "Manage my consent" is an authenticated application allowing the user to review and revoke consent.
  It has an admin function to review all consent.


.flow "happy path"
image::docs/flow.svg[]


## Structure

.Internal structure
image::docs/structure.svg[]


## Persistence

Using the standard Django ORM a number of databases are supported.

## Deployment

The recommended deployment uses the docker image provided in the github repo d-simpleconsent


## Access Control

The HTTP port of the Django application must only be accessible by SATOSA and the SP proxy.
There is no authentication in Django itself.


