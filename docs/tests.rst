Running Debmetrics Tests
************************

To run the tests, run `nosetests3` from anywhere within the directory
structure of debmetrics.

Before running the tests, you should edit .debmetrics.ini to have the TEST
flag set True. The TEST flag causes debmetrics to use the metrics_test schema
instead of the metrics schema like normal. That way the normal data is not
disturbed by the test data. After setting the flag, delete all the model files
in debmetrics/models/ and regenerate the models by running make in the root of
debmetrics.

After you are done running the tests, you should set the TEST flag to False
and repeat the above steps.
