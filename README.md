# optimizely-extensions-cli
CLI for managing Optimizely Extensions

**Opt-Extend** is a CLI to simplift interacting with Optimizely Extensions programmatically.
More documentation to come.


Usage Examples
==============

Authenticating with Personal Access Tokens
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To authenticate with the Optimizely REST API, the **authorize** command configures a file at $HOME/.optimizely-config.cfg that can hold multiple project ID and personal access token pairs, which can be
removed with the **unauthorize** command. If a project_id that does not appear in the auth config is passed as a command argument, a prompt will
be used to get a personal access token at the time of execution.

To generate a personal access token, use this
.. _reference: https://help.optimizely.com/Integrate_Other_Platforms/Generate_a_personal_access_token_in_Optimizely_X_Web


To access project 1322423 until you remove the token from memory later with **unauthorize**::

    $ opt-extend authorize 1322423 <personal_access_token>
    /   Added authorization for project 1322423


Now, future commands that reference project 1322423 will be authorized without requiring a prompt for your personal access token (as long as the token is not revoked and
has permissions for the actions you are performing).


To unauthorize a specific project::

    $ opt-extend unauthorize --project-id=09138432
    /   Removed authorization for project 09138432

To unauthorize all projects::

    $ opt-extend unauthorize --all
    /   Removed all authorization tokens from configuration.



Initializing a directory to contain a new Extension (in a format that can be directly ingested by the upload command when ready)::

    $ opt-extend initialize $PROJECT_ID ~/my_extension_directory my_edit_url.com --description='This extension rocks' --name='My First Extension'
    /	Initialized directory /Users/<>/my_extension_directory to contain My First Extension

Upload the Extension contained in a directory to Optimizely and enable the Extension::

    $ opt-extend upload ~/my_extension_directory --enable
    /	Successfully created new Extension 983489

Accumulate data on the current uses of a specified Extension, filtering for Extensions running on a certain page::

    $ opt-extend extension_data $PROJECT_ID $EXTENSION_ID --page_id=907342
    /   Experiment Name       Experiment ID    Variation Name   Variation ID    Variation Status     Page ID
    /   =====================================================================================================
    /   Homepage Experiment   1430897324       Original         990934340        Archived            907342
    /   Search Experiment     2342342344       Var 1            902734099        Running             907342

Disable all Extensions in a project containing a match to a ceratin regex string::

    $ opt-extend disable $PROJECT_ID --grep='https://language.googleapis.com'
    /   Disabled Extension 23049243: Sentiment Reaction Modal
    /   Disabled Extension 29008123: Google Translate Search Translator

