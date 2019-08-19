= Security Considerations


== Manipulation of the frontend database (e..g via REST API)

An EntityDescriptor is published by PEP writing the file to the PEPOUT directory.
The control depends on the validation process in pep.py, which requires a valid XML signature.
The status in the frontend database is not relevant, 
therefore any potential manipulation on the frontend (.e.g. setting the status to 'accepted') 
will not make that attack succeed. 

However, access to the operation kwarg of MDStatment.save() should be blocked for REST API clients.