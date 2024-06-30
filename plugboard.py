from constants import ALPHABET


class Plugboard:
    def __init__(self) -> None:
        self.plugboard_changes = {}

    def add_connections(self, new_connections: str):
        connections_added: list[str] = []
        failed_connections: list[str] = []
        splitted_connections = new_connections.split(",")

        for connection in splitted_connections:
            connection = connection.strip()
            if len(connection) != 2:
                failed_connections.append(connection)
                continue
            if connection[0] == connection[1]:
                failed_connections.append(connection)
                continue
            first_param_index = ALPHABET.index(connection[0])
            second_param_index = ALPHABET.index(connection[1])
            if first_param_index == -1 or second_param_index == -1:
                failed_connections.append(connection)
                continue
            if (
                first_param_index in self.plugboard_changes
                or second_param_index in self.plugboard_changes
            ):
                failed_connections.append(connection)
                continue
            self.plugboard_changes[first_param_index] = second_param_index
            self.plugboard_changes[second_param_index] = first_param_index
            connections_added.append(connection)

        print(
            f"Succesfully added {len(connections_added)} connections: {connections_added}. "
        )
        print(f"This connections failed: {failed_connections}.")

    def get_num_for(self, char_idx: int):
        if not char_idx in self.plugboard_changes:
            return char_idx
        return self.plugboard_changes[char_idx]
