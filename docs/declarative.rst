Declarative Workflows
=====================

Once you have your collection of Routines, you can describe the workflow itself
with a `yaml` file.

The `yaml` file is a collection of descriptions of your routines. There are
three important aspects of a routine description:

1. The label. Other routines will refer to it by this label.
2. The `data` property. Specifies from which other routine it gets the data it
   acts on.
3. The other properties. They will be passed as constructor arguments to the
   properties.


The Label
---------

The label must simply be a valid json label. Alpha-numeric plus underscores,
starting with a letter.


The Data Property
-----------------

The `data` property has one required sub-property, `from`. `from` can name
another routine in the yaml workflow, or an external routine. External routines
are detected by the presence of a dot (`.`) in the value.

Aditional sub-properties are allowed on `data`. They will be passed as arguments
when the data is accessed. For example, a routine which filters the data might
take a boolean argument when accessed, to toggle whether to provide rows which
were matched or unmatched.

For `from` properties containg `.`s, the following strategy is used to try and
access the routine:

1. Look for a `.yaml` files in the current directory with a name matching the
   label preceding the last `.`, with a routine matching the label following the
   last `.`.
2. Try to import a module using the the part of the label preceding the last
   `.`, with an importable object matching the label following the last `.`.



