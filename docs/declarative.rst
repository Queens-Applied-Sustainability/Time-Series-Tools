.. role:: bash(code)
    :language: bash

Declarative Workflows
=====================

Once you have your collection of Routines, you can describe the workflow itself
with a :code:`yaml` file.


The YAML file
-------------

The :code:`yaml` file is a collection of descriptions of your routines. There
are three important aspects of a routine description:

1. The label. Other routines will refer to it by this label.
2. The :code:`data` property. Specifies from which other routine it gets the
   data it acts on.
3. The other properties. They will be passed as constructor arguments to the
   properties.


The Label
^^^^^^^^^

The label must simply be a valid json label. Alpha-numeric plus underscores,
starting with a letter.


The Data Property
^^^^^^^^^^^^^^^^^

The :code:`data` property has one required sub-property, :code:`from`.
:code:`from` can name another routine in the yaml workflow, or an external
routine. External routines are detected by the presence of a dot (:code:`.`) in
the value.

Aditional sub-properties are allowed on :code:`data`. They will be passed as
arguments when the data is accessed. For example, a routine which filters the
data might take a boolean argument when accessed, to toggle whether to provide
rows which were matched or unmatched.

For :code:`from` properties containg :code:`.`, the following strategy is used
to try and access the routine:

1. Look for a :code:`.yaml` files in the current directory with a name matching
   the label preceding the last :code:`.`, with a routine matching the label
   following the last :code:`.`.
2. Try to import a module using the the part of the label preceding the last
   :code:`.`, with an importable object matching the label following the last
   :code:`.`.


Additional Properties
^^^^^^^^^^^^^^^^^^^^^

Any additional properties will tell the routine about itself when created.


Running a Workflow
------------------

Run the whole thing: :bash:`timeflow workflow.yaml`

Run a routine (and all its dependencies): :bash:`timeflow workflow.yaml routine`

Specifiy what sort of output you want: :bash:`timeflow workflow -o csv`

 * The label after the :code:`-o` file will first try to use a builtin timeflow,
   or try to import an export routine if it contains a dot.

