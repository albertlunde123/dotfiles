from encoding import encode_points
from ase import Atoms
from ase.calculators.emt import EMT 
import numpy as np
import json

# ----------------------------------------------
# Functions for managing the database
# ----------------------------------------------

# Function to check if a configuration exists and get its energy

def check_configuration_exists(conn, config_str):
    cursor = conn.cursor()
    cursor.execute("SELECT energy FROM configurations WHERE configuration = ?", (config_str,))
    row = cursor.fetchone()
    return row[0] if row else None

# Function to insert a new encoded configuration and its energy, aswell as inserting the raw configuration
def insert_configuration(conn, config_str, encoded_conf, energy):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO configurations (configuration, energy) VALUES (?, ?)", (encoded_conf, energy))
    cursor.execute("INSERT INTO actual_points (points, energy) VALUES (?, ?)", (config_str, energy))
    conn.commit()

def fetch_raw_configurations(conn):

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM actual_points")
    rows = cursor.fetchall()

    points = []
    energies = []
    for row in rows:
        points.append(np.array(json.loads(row[0])).flatten())
        energies.append(row[1])

    return points, energies

def calculate_energy(configuration, element = 'Au'):

    n_atoms = int(len(configuration))
    positions = np.zeros((n_atoms, 3))
    if configuration.ndim == 1:
        configuration = configuration.reshape((n_atoms, 2))

    positions[:, :2] = configuration
    atoms = Atoms(f"{element}{n_atoms}", positions=positions)
    
    # Set the calculator to EMT
    atoms.calc = EMT()
    return atoms.get_potential_energy()

# ----------------------------------------------
# Functions for storing and calculating energy
# ----------------------------------------------

def store_energy(configuration, conn):

    # Encode the configuration for storage
    if configuration.ndim == 1:
        configuration = configuration.reshape((int(len(configuration)/2), 2))

    encoded_conf = encode_points(configuration)
    regular_conf = json.dumps(configuration.tolist())

    # Check if the configuration exists

    energy = check_configuration_exists(conn, encoded_conf)

    if energy is None:
        # Calculate the energy
        energy = calculate_energy(configuration)
        insert_configuration(conn, regular_conf, encoded_conf, energy)

    return energy
