import pandas as pd
from structural_analysis import Structure
from abc import ABCMeta, abstractmethod
import numpy as np


class Table(metaclass=ABCMeta):
    display_precision = 4

    def __init__(self, structure: Structure):
        self.structure = structure
        self.dataframe = None
        pd.set_option("display.precision", Table.display_precision)

    @abstractmethod
    def _populate_data(self):
        raise NotImplementedError

    def print(self):
        print(self.dataframe)

    def write_to_txt(self, path=""):
        self.dataframe.to_csv(f"{path}/{self.structure.name}_nodal_displacements.txt", sep='\t', index=False,
                              float_format=f'%.{Table.display_precision}f')

    def write_to_csv(self, path=""):
        self.dataframe.to_csv(f"{path}/{self.structure.name}_reactions.csv", sep=',', index=False,
                              float_format=f'%.{Table.display_precision}f')


class DisplacementTable(Table):
    def __init__(self, structure: Structure):
        super().__init__(structure)
        self.dataframe = pd.DataFrame(columns=["Node", "X Displacement", "Y Displacement", "Z Displacement",
                                               "X Rotation", "Y Rotation", "Z Rotation"])
        self._populate_data()

    def _populate_data(self):
        counter = 0
        for node in self.structure.nodes:
            self.dataframe.loc[counter] = [node.id, node.dof_x.displacement, node.dof_y.displacement,
                                           node.dof_z.displacement, node.dof_rx.displacement,
                                           node.dof_ry.displacement, node.dof_rz.displacement]
            counter += 1
        self.dataframe = self.dataframe.astype({'Node': np.int})


class ReactionsTable(Table):
    def __init__(self, structure: Structure):
        super().__init__(structure)
        self.dataframe = pd.DataFrame(columns=["Node", "X Force", "Y Force", "Z Force",
                                               "X Moment", "Y Moment", "Z Moment"])
        self._populate_data()

    def _populate_data(self):
        counter = 0
        for node in self.structure.nodes:
            self.dataframe.loc[counter] = [node.id, node.dof_x.force, node.dof_y.force, node.dof_z.force,
                                           node.dof_rx.force, node.dof_ry.force, node.dof_rz.force]
            counter += 1
        self.dataframe = self.dataframe.astype({'Node': np.int})
