# Portal Admin tool (Metadata Registry)

## Functionality

Users can manage metadata statements (MDS). 
An MDS comprises an EntityDescriptor (ED) with a few attributes to manage status and disposition (add/replace and delete). 

Actions:
- list/search existing MDS
- Show details and history
- add a new MDS
- replace an existing one with a newer version
- delete an MDS

Users need to sign the ED for add, replace and modify, unless the uploaded ED has a valid signature. 

Implementation for the WebUI:

The model defines data that finally resides in git. To synchronize git and the db, git is loaded into the db on login,
or with manual refresh.

On activating a changeview a CheckOut record is created, 
and the MDS record is updated to have a foreign key to CheckOut.
The Checkout record is deleted by garbage collection or on logout. 

This function is implemented by registering a reveiver in receivers.py. 
The MDS ModelAdmin extends the change_view to send the signal.