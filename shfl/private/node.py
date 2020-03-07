import copy

from shfl.private.data import UnprotectedAccess


class DataNode:
    """
    This class represents an independent data node.

    A DataNode has its own private data and provides methods
    to initialize this data and access. The access to private data needs to be configured with an access policy
    before query it or an exception will be raised. A method to transform private data is also provided. This is
    a mechanism that allows data preprocessing or related task over data.

    A model (see: [Model](../../Model)) can be deployed in the DataNode and use private data
    in order to learn. It is assumed that a model is represented by its parameters and the access to this parameters
    must be also configured before queries.
    """

    def __init__(self):
        self._private_data = {}
        self._private_data_access_policies = {}
        self._model = None
        self._model_access_policy = UnprotectedAccess()

    @property
    def model(self):
        print("You can't get the model, you need to query the params to access")
        print(type(self._model))
        print(self._model)

    @model.setter
    def model(self, model):
        """
        Sets the model to use in the node

        # Arguments:
            model: Instance of a class implementing ~TrainableModel
        """
        self._model = model

    @property
    def private_data(self):
        """
        Allows to see data for this node, but you cannot retrieve data

        # Returns
            private : test data
        """
        print("Node private data, you can see the data for debug purposes but the data remains in the node")
        print(type(self._private_data))
        print(self._private_data)

    def set_private_data(self, name, data):
        """
        Creates copy of data in private memory using name as key. If there is a previous value with this key the
        data will be override.

        # Arguments:
            name: String with the key identifier for the data
            data: Data to be stored in the private memory of the DataNode
        """
        self._private_data[name] = copy.deepcopy(data)

    def configure_private_data_access(self, name, data_access_definition):
        """
        Adds a DataAccessDefinition for a concrete private data.

        # Arguments:
            name: String with the key identifier for the data
            data_access_definition: Policy to access data (see: [DataAccessDefinition](../DataAccessDefinition))
        """
        self._private_data_access_policies[name] = copy.deepcopy(data_access_definition)

    def configure_model_params_access(self, data_access_definition):
        """
        Adds a DataAccessDefinition for model parameters.

        # Arguments:
            data_access_definition: Policy to access parameters (see: [DataAccessDefinition](../DataAccessDefinition))
        """
        self._model_access_policy = copy.deepcopy(data_access_definition)

    def apply_data_transformation(self, private_property, federated_transformation):
        """
        Executes FederatedTransformation (see: [Federated Operation](../Federated Operation)) over private date.

        # Arguments:
            name: String with the key identifier for the data
            federated_transformation: Operation to execute (see: [Federated Operation](../Federated Operation))
        """
        federated_transformation.apply(self._private_data[private_property])

    def query_private_data(self, private_property):
        """
        Queries private data previously configured. If the access didn't configured this method will raise exception

        # Arguments:
            name: String with the key identifier for the data
        """
        if private_property not in self._private_data_access_policies:
            raise ValueError("Data access must be configured before query data")

        data_access_policy = self._private_data_access_policies[private_property]
        data = data_access_policy.query.get(self._private_data[private_property])
        return data_access_policy.dp_mechanism.randomize(data)

    def query_model_params(self):
        """
        Queries model parameters. By default the parameters access is unprotected but access definition can be changed
        """
        return self._model_access_policy.query.get(self._model.get_model_params())

    def set_model_params(self, model_params):
        """
        Sets the model to use in the node

        # Arguments:
            model_params: Parameters to set in the model
        """
        self._model.set_model_params(model_params)

    def train_model(self, training_data_key):
        """
        Train the model that has been previously set in the data node

        # Arguments:
            training_data_key: String identifying the private data to use for this model. This key must contain
            LabeledData (see: [Data](../../Data))
        """
        labeled_data = self._private_data.get(training_data_key)
        if not hasattr(labeled_data, 'data') or not hasattr(labeled_data, 'label'):
            raise ValueError("Private data needs to have 'data' and 'label' to train a model")
        self._model.train(labeled_data.data, labeled_data.label)

    def predict(self, data):
        """
        Uses the model to predict new data

        # Arguments:
            data: Data to predict
        """
        return self._model.predict(data)