from enigma_disk import EnigmaDisk
from plugboard import Plugboard
from constants import ALPHABET, DISK_KEYS


disk_amount = len(DISK_KEYS)


def app():
    try:
        configuration = getConfiguration()
        selected_disks: tuple = configuration.get("selected_disks")
        disks_rotation: tuple = configuration.get("disks_rotation")
        plugboard: Plugboard = configuration.get("plugboard")

        disks = [
            EnigmaDisk(
                DISK_KEYS[selected_disks[0]],
                rotation=disks_rotation[0],
            ),
            EnigmaDisk(
                DISK_KEYS[selected_disks[1]],
                rotation=disks_rotation[1],
            ),
            EnigmaDisk(
                DISK_KEYS[selected_disks[2]],
                rotation=disks_rotation[2],
            ),
        ]
        deflector = EnigmaDisk("ZYXWVUTSRQPONMLKJIHGFEDCBA")

        entered_text = (
            input("\nEnter the text to encrypt (chars from A-Z): ").strip().upper()
        )
        output_text = encryptText(entered_text, disks, plugboard, deflector)
        print("\n", output_text, sep="")

    except ValueError:
        print("\nInvalid input, use numbers.")

    except IndexError as e:
        print("\n" + str(e))

    except KeyboardInterrupt:
        return True

    except:
        print("\nThere was an important error. Try again.")


def getConfiguration() -> dict[str]:
    disk_input_help_text = "Enter the disk in position A (0-%s): " % (disk_amount - 1)
    disk_1 = int(input("\n" + disk_input_help_text))
    disk_2 = int(input(disk_input_help_text))
    disk_3 = int(input(disk_input_help_text))
    disks_range = range(disk_amount)

    if not (disk_1 in disks_range and disk_2 in disks_range and disk_3 in disks_range):
        raise IndexError(
            "Invalid disk selection, use numbers between 0 and %s" % (disk_amount - 1)
        )

    disk_1_offset = int(input("\nEnter disk A rotation (0-25): "))
    disk_2_offset = int(input("Enter disk B rotation (0-25): "))
    disk_3_offset = int(input("Enter disk C rotation (0-25): "))
    disk_rotation_range = range(26)

    if not (
        disk_1_offset in disk_rotation_range
        and disk_2_offset in disk_rotation_range
        and disk_3_offset in disk_rotation_range
    ):
        raise IndexError("Invalid disk rotation input, use numbers between 0 and 25.")

    plugboard = Plugboard()

    while True:
        wants_to_add_pb_change = (
            input("\nDo you want to add plugboard changes? (y/n): ").strip().lower()
            == "y"
        )
        if not wants_to_add_pb_change:
            break
        changes_to_add = (
            input(
                "Specify the connections using the syntax 'XY'. Separate them with commas. (A-Z): "
            )
            .strip()
            .upper()
        )
        plugboard.add_connections(changes_to_add)

    return {
        "selected_disks": (disk_1, disk_2, disk_3),
        "disks_rotation": (disk_1_offset, disk_2_offset, disk_3_offset),
        "plugboard": plugboard,
    }


def encryptText(
    entered_text: str,
    disks: list[EnigmaDisk],
    plugboard: Plugboard,
    deflector: EnigmaDisk,
) -> str:
    encrypted_text = ""

    for char in entered_text:
        if char == " " or char.isnumeric():
            encrypted_text += char
            continue

        disks[2].rotate()
        if disks[2].rotation == 0:
            disks[1].rotate()
            if disks[1].rotation == 0:
                disks[0].rotate()

        char_value = ALPHABET.find(char)
        if char_value == -1:
            print("Invalid characters in input text.")
            raise
        current_output = plugboard.get_num_for(char_value)
        for i in range(2, -1, -1):
            current_output = disks[i].get_num(current_output)
        current_output = deflector.get_num(current_output)
        for i in range(3):
            current_output = disks[i].get_num(current_output, True)
        current_output = plugboard.get_num_for(current_output)
        encrypted_text += ALPHABET[current_output]

    return encrypted_text


while True:
    isExitting = app()
    if isExitting:
        print("\nExitting...\n")
        break
    print("Restarting app...\n")
    print("----------------------\n")
