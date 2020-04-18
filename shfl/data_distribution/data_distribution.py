import numpy as np
import random
import abc

from shfl.private.data import LabeledData
from shfl.private.federated_operation import FederatedData
from shfl.private.node import DataNode


class DataDistribution(abc.ABC):
    """
    Abstract class for data distribution

    # Arguments:
        database: Database to distribute. (see: [Databases](../../Databases))
    """

    def __init__(self, database):
        self._database = database

    def get_federated_data(self, num_nodes, percent=100, weights=None):
        """
        Method that split the whole data between the established number of nodes.

        # Arguments:
            num_nodes: Number of nodes to create
            percent: Percent of the data (between 0 and 100) to be distributed (default is 100)
            weights: Array of weights for weighted distribution (default is None)

        # Returns:
              * **federated_data, test_data, test_label**
        """

        train_data, train_label = self._database.train
        validation_data, validation_label = self._database.validation
        test_data, test_label = self._database.test

        train_data = np.concatenate((train_data, validation_data), axis=0)
        train_label = np.concatenate((train_label, validation_label), axis=0)

        federated_train_data, federated_train_label = self.make_data_federated(train_data,
                                                                               train_label,
                                                                               num_nodes, percent,
                                                                               weights)

        federated_data = FederatedData()
        for node in range(num_nodes):
            node_data = LabeledData(federated_train_data[node], federated_train_label[node])
            federated_data.add_data_node(node_data)

        return federated_data, test_data, test_label

    @abc.abstractmethod
    def make_data_federated(self, data, labels, num_nodes, percent, weights):
        """
        Method that must implement every data distribution extending this class

        # Arguments:
            data: Array of data
            labels: Labels
            num_nodes : Number of nodes
            percent: Percent of the data (between 0 and 100) to be distributed (default is 100)
            weights: Array of weights for weighted distribution (default is None)

        # Returns:
            federated_data: Data for each client
            federated_label: Labels for each client
        """
