# optimizely-extensions-cli
CLI for managing Optimizely Extensions

**Opt-Extend** is a CLI to simplift interacting with Optimizely Extensions programmatically.
More documentation to come.


Usage Examples
==============

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

To authenticate with the Optimizely REST API, the **authorize** command configures a file at $HOME/.optimizely-config.cfg that can hold many project ID and personal access token pairs, which can be
removed with the **unauthorize** command. If a project_id argument is passed that does not appear in the auth config, a prompt will
be used to get a personal access token. To generate a personal access token, use the [API Reference](https://help.optimizely.com/Integrate_Other_Platforms/Generate_a_personal_access_token_in_Optimizely_X_Web).

This will allow you to access project 09138432 until you remove the token from memory later with **unauthorize**::

    $ opt-extend authorize 09138432 2:976b1f28hGCUcc1G5U0l9pasfjdsiflkajsdfa9aufd
    /   Added authorization for project 09138432

To unauthorize a specific project::

    $ opt-extend unauthorize --project-id=09138432
    /   Removed authorization for project 09138432

To unauthorize all projects::

    $ opt-extend unauthorize --all
    /   Removed all authorization tokens from configuration.
