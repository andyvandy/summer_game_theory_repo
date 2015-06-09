# log_utils.py
# Contains functions for building log files

import os

def ensure_directory(directory):
    """Ensures that directory exists and is empty. Be careful with this.
    Code used from: 
    http://stackoverflow.com/questions/185936/delete-folder-contents-in-python
    http://stackoverflow.com/questions/273192/in-python-check-if-a-directory-exists-and-create-it-if-necessary

    Args:
        directory: the directory to create/clear
    """

    if not os.path.exists(directory):
        os.makedirs(directory)

    for the_file in os.listdir(directory):
        file_path = os.path.join(directory, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception, e:
            print e


def write_gen_number(log_file, gen_number):
    """Writes the generation number into the log file.

    Args:
        log_file: the log file object to write to
        gen_number: an int specifying the current generation
    """

    log_file.write("Generation ")
    log_file.write(str(gen_number))
    log_file.write("\n\n")


def write_round_number(log_file, round_number):
    """Writes the round number into the log file.

    Args:
        log_file: the log file object to write to
        round_number: an int specifying the current round
    """

    log_file.write("Round ")
    log_file.write(str(round_number))
    log_file.write("\n\n")


def write_matchup_header(log_file, matchup_number, agent_1_ID, agent_2_ID):
    """Writes the header for the matchup into the log file.

    Args:
        log_file: the log file object to write to
        matchup_number: an int specifying the current matchup
        agent_1_ID: a tuple specifying the ID of agent 1
        agent_2_ID: a tuple specifying the ID of agent 2
    """

    log_file.write("Matchup number ")
    log_file.write(str(matchup_number))
    log_file.write(": Agent ")
    log_file.write(str(agent_1_ID))
    log_file.write(" vs. Agent ")
    log_file.write(str(agent_2_ID))
    log_file.write(".\n")

def write_turn_info(log_file, turn_number, investor_ID, trustee_ID, 
                    investor_cash, trustee_cash, investor_gift, trustee_gift, 
                    B, C):
    """Writes the information for a turn into the log file.

    Args:
        log_file: the log file object to write to
        turn_number: an int specifying the current turn
        investor_ID: a tuple specifying the ID of the investor
        trustee_ID: a tuple specifying the ID of the trustee
        investor_cash: an int specifying the cash the investor has at the 
            beginning of the turn
        trustee_cash: an int specifying the cash the trustee has at the 
            beginning of the turn
        investor_gift: an int specifying the gift investor -> trustee
        trustee_gift: an int specifying the gift trustee -> investor
    """

    log_file.write("Turn number ")
    log_file.write(str(turn_number))
    log_file.write(". Agent ")
    log_file.write(str(investor_ID))
    log_file.write(" has ")
    log_file.write(str(investor_cash))
    log_file.write(". Agent ")
    log_file.write(str(trustee_ID))
    log_file.write(" has ")
    log_file.write(str(trustee_cash))
    log_file.write(".\n")
    log_file.write("Agent ")
    log_file.write(str(investor_ID))
    log_file.write(" gives ")
    log_file.write(str(investor_gift))
    log_file.write(", Agent ")
    log_file.write(str(trustee_ID))
    log_file.write(" receives ")
    log_file.write(str(investor_gift * B))
    log_file.write(".\nAgent ")
    log_file.write(str(trustee_ID))
    log_file.write(" gives ")
    log_file.write(str(trustee_gift))
    log_file.write(", Agent ")
    log_file.write(str(investor_ID))
    log_file.write(" receives ")
    log_file.write(str(trustee_gift * C))
    log_file.write(".\n")