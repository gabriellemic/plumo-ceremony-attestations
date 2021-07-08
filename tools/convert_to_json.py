import re
import json

round_started = False
round = ''
round_number = 0
phase_number = 0
details = { "phase1": [], "phase2": [] }
for line in open('README.md').readlines():
  if 'Phase' in line:
    phase_number += 1

  if 'Round' in line or ('Phase' in line and phase_number >= 1):
    if round_number == 0:
      round_number += 1
      round_started = True
      continue

    round_number += 1
    round_started = True
    round_dict = {}
    for round_line in round.split('\n')[4:]:
      participant = list(map(lambda x: x.strip(), round_line.split('|')))
      if len(participant) == 1:
        continue
      twitter = re.search('\[Twitter\]\((.*?)\)', participant[5])
      keybase = re.search('\[Keybase\]\((.*?)\)', participant[5])
      github = re.search('\[Github\]\((.*?)\)', participant[5])
      gist = re.search('\[Gist\]\((.*?)\)', participant[5])
      round_dict[participant[2]] = {
        'name': participant[3],
        'affiliation': participant[4] if len(participant[4]) > 0 else None,
        'twitter': twitter.groups()[0] if twitter is not None else None,
        'keybase': keybase.groups()[0] if keybase is not None else None,
        'github': github.groups()[0] if github is not None else None,
        'gist': gist.groups()[0] if gist is not None else None,
      }
    details["phase" + str(phase_number)].append(round_dict)
    round = ''

  if round_started:
    round += line

print(json.dumps(details))
