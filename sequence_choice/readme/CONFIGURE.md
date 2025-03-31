Activate *Use Custom Sequences*.

1. Go to *Settings \> General Settings \> Permissions*.
2. Activate *Use Custom Sequences* and save.

Open a model, select a field to store sequence in, select a field to choose sequence by.

1. Follow the link to *Settings \> Technical \> Database Structure \> Models*.
2. Click on a model to open it.
3. Decide which field to store the sequence code in. 
4. *Store sequence in*: Set the field to store the sequence code. Hover ? for more info.
   Make a new field if necessary. The type should be 'char' or 'text'.
5. Save. A default sequence will be created.
6. *Choose sequence by*: Set the field to choose a sequence. Hover ? for more info.
   Make a new field if necessary. The type should be 'selection' or 'boolean'.
7. Save. A sequence will be created for each field option.

Go to Sequences, and customize them.

* Go to *Settings \> Technical \> Sequences & Identifiers \> Sequences*.

The default sequence (code=model.name) is used when:

* The model has no field to choose a sequence.
* There is a 'selection' field to choose a sequence, and the record has empty value.

If the default sequence is deleted,
and the model field to *store sequence in* is updated,
then the default sequence will be created again.
