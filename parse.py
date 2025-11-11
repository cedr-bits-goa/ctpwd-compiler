def _parse_if(blocks, i):
    cond = blocks[i + 1].get("value") if i + 1 < len(blocks) and blocks[i + 1]["type"] == "condition" else None
    action = blocks[i + 2].get("value") if i + 2 < len(blocks) and blocks[i + 2]["type"] == "action" else None
    entry = {"if": cond, "action": action}
    seq = ["if"] + ([cond] if cond else []) + ([action] if action else [])
    return entry, seq, i + 3


def _parse_elseif(blocks, i):
    cond = blocks[i + 1].get("value") if i + 1 < len(blocks) and blocks[i + 1]["type"] == "condition" else None
    action = blocks[i + 2].get("value") if i + 2 < len(blocks) and blocks[i + 2]["type"] == "action" else None
    entry = {"elseif": cond, "action": action}
    seq = ["elseif"] + ([cond] if cond else []) + ([action] if action else [])
    return entry, seq, i + 3


def _parse_else(blocks, i):
    if i + 1 < len(blocks) and blocks[i + 1]["type"] == "control" and blocks[i + 1]["value"] == "if":
        cond = blocks[i + 2].get("value") if i + 2 < len(blocks) and blocks[i + 2]["type"] == "condition" else None
        action = blocks[i + 3].get("value") if i + 3 < len(blocks) and blocks[i + 3]["type"] == "action" else None
        entry = {"elseif": cond, "action": action}
        seq = ["elseif"] + ([cond] if cond else []) + ([action] if action else [])
        return entry, seq, i + 4
    else:
        action = blocks[i + 1].get("value") if i + 1 < len(blocks) and blocks[i + 1]["type"] == "action" else None
        entry = {"else": action}
        seq = ["else"] + ([action] if action else [])
        return entry, seq, i + 2


def parse_blocks(blocks, loop_count, colors_from_image=None):
    colors, conditions, sequence = [], [], []
    i = 0
    n = len(blocks)

    while i < n:
        b = blocks[i]
        t, v = b.get("type"), b.get("value")

        # --- NEW: Maze & Direction support ---
        if t in {"maze", "direction"}:
            sequence.append(b)
            i += 1
            continue

        # --- Existing logic ---
        if t == "loop":
            i += 1
            continue

        if t == "control":
            if v == "if":
                entry, seq, i = _parse_if(blocks, i)
                conditions.append(entry)
                sequence.extend(seq)
                continue
            elif v == "elseif":
                entry, seq, i = _parse_elseif(blocks, i)
                conditions.append(entry)
                sequence.extend(seq)
                continue
            elif v == "else":
                entry, seq, i = _parse_else(blocks, i)
                conditions.append(entry)
                sequence.extend(seq)
                continue
            else:
                sequence.append(v)
                i += 1
                continue

        if t == "color":
            colors.append(v)
            sequence.append(v)
            i += 1
            continue

        if t in {"condition", "action", "label"}:
            sequence.append(v)
            i += 1
            continue

        i += 1

    # --- Fixed Loop Expansion ---
    if loop_count > 1:
        if sequence:  # if there is any sequence (conditions, actions, or colors)
            expanded_sequence = sequence * loop_count
        else:  # only pure colors case
            expanded_sequence = colors * loop_count
    else:
        expanded_sequence = sequence if sequence else colors

    return {
        "colors": colors,
        "loop_count": loop_count,
        "conditions": conditions,
        "sequence": expanded_sequence
    }
