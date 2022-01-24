def trim_whitespace(strs):

    return [x.replace(' ', '').replace('\n', '').replace('\t', '') for x in strs]

print(trim_whitespace(['dsfh sfdgh fsgh fs\ngj fsghj tryj ', 'sgf dfah rth rs     hj tyj', 'asfdg dfag ,erg.']))
