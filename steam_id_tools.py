import re


def to_steamID(steamID):
    id_str = str(steamID)

    if id_str.isnumeric() and not len(id_str) == 17:
        id_str = f"[U:1:{id_str}]"

    if re.search("^STEAM_", id_str): # Already a steamID
        return id_str

    elif re.search("^\[.*\]$", id_str): # If passed steamID3

        id_split = id_str.split(":") # Split string into 'Universe', Account type, and Account number
        account_id3 = int(id_split[2][:-1]) # Remove ] from end of steamID3

        if account_id3 % 2 == 0:
            account_type = 0
        else:
            account_type = 1

        account_id = (account_id3 - account_type) // 2
        return "STEAM_0:" + str(account_type) + ":" + str(account_id)

    elif id_str.isnumeric(): # Passed steamID64

        id64_base = 76561197960265728 # steamID64 are all offset from this value
        offset_id = int(id_str) - id64_base

        # Get the account type and id
        if offset_id % 2 == 0:
            account_type = 0
        else:
            account_type = 1

        account_id = ((offset_id - account_type) // 2)

        return "STEAM_0:" + str(account_type) + ":" + str(account_id)
    else:
        raise ValueError(f"Wrong steam_id format: {id_str}")


def to_numeric_string(steam_id):
    if (isinstance(steam_id, float) or steam_id.isnumeric()):
        return str(int(steam_id))
    return str(steam_id)