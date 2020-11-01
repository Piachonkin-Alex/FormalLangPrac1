from types import SimpleNamespace

FiniteAutomation = SimpleNamespace  # Everything is a SimpleNamespace
Transmission = SimpleNamespace


def automation_from_expression(expression: str) -> FiniteAutomation:
    next_state_name = 0  # counter for all states in
    stack_of_automation = []
    for symbol in expression:
        if symbol == '.':
            right_expr = stack_of_automation.pop()
            left_expr = stack_of_automation.pop()
            concat_automation = FiniteAutomation()
            concat_automation.states = left_expr.states
            concat_automation.states += right_expr.states
            concat_automation.start = left_expr.start
            concat_automation.finish = right_expr.finish
            concat_automation.transmissions = left_expr.transmissions
            concat_automation.transmissions += right_expr.transmissions
            bridge = Transmission(
                from_=left_expr.finish,
                to_=right_expr.start,
                by=''
            )
            concat_automation.transmissions.append(bridge)
            stack_of_automation.append(concat_automation)
        elif symbol == '+':
            right_expr = stack_of_automation.pop()
            left_expr = stack_of_automation.pop()
            sum_automation = FiniteAutomation()
            sum_automation.states = left_expr.states
            sum_automation.states += right_expr.states
            sum_automation.states.append(next_state_name)
            sum_automation.states.append(next_state_name + 1)
            sum_automation.start = next_state_name
            sum_automation.finish = next_state_name + 1
            sum_automation.transmissions = left_expr.transmissions
            sum_automation.transmissions += right_expr.transmissions
            from_start_to_left = Transmission(
                from_=next_state_name,
                to_=left_expr.start,
                by=''
            )
            sum_automation.transmissions.append(from_start_to_left)
            from_start_to_right = Transmission(
                from_=next_state_name,
                to_=right_expr.start,
                by=''
            )
            sum_automation.transmissions.append(from_start_to_right)
            from_left_to_end = Transmission(
                from_=left_expr.finish,
                to_=next_state_name + 1,
                by=''
            )
            sum_automation.transmissions.append(from_left_to_end)
            from_right_to_end = Transmission(
                from_=right_expr.finish,
                to_=next_state_name + 1,
                by=''
            )
            sum_automation.transmissions.append(from_right_to_end)
            stack_of_automation.append(sum_automation)
            next_state_name += 2
        elif symbol == "1":
            empty_automation = FiniteAutomation()
            empty_automation.states = [next_state_name]
            empty_automation.start = next_state_name
            empty_automation.finish = next_state_name
            empty_automation.transmissions = []
            next_state_name += 1
            stack_of_automation.append(empty_automation)
        elif symbol == "*":
            star_automation = stack_of_automation.pop()
            if star_automation.start == star_automation.finish:
                stack_of_automation.append(star_automation)
                continue
            finish_to_start_edge = Transmission(
                from_=star_automation.finish,
                to_=star_automation.start,
                by=''
            )
            star_automation.transmissions.append(finish_to_start_edge)
            star_automation.finish = star_automation.start
            stack_of_automation.append(star_automation)
        else:
            base_automation = FiniteAutomation()
            base_automation.states = [next_state_name, next_state_name + 1]
            base_automation.start = next_state_name
            base_automation.finish = next_state_name + 1
            edge = Transmission(
                from_=next_state_name,
                to_=next_state_name + 1,
                by=symbol
            )
            base_automation.transmissions = [edge]
            next_state_name += 2
            stack_of_automation.append(base_automation)
    return stack_of_automation.pop()


def remove_empty_transmissions(automation: FiniteAutomation) -> FiniteAutomation:
    new_automation = FiniteAutomation()
    new_automation.transmissions = []
    reachable_list = []

    one_letter_transmissions = []

    def dfs_for_one_letter_transmissions(start_state, cur_state):
        if cur_state in reachable_list:
            return
        for edge in automation.transmissions:
            if edge.from_ == cur_state:
                if edge.by != '':
                    new_transmission = Transmission(
                        from_=start_state,
                        to_=edge.to_,
                        by=edge.by
                    )
                    one_letter_transmissions.append(new_transmission)
                else:
                    dfs_for_one_letter_transmissions(start_state, edge.to_)

    for state in automation.states:
        dfs_for_one_letter_transmissions(state, state)
        reachable_list = []

    new_automation.start = automation.start
    new_automation.states = []

    def dfs_for_states(vertex):
        if vertex in new_automation.states:
            return
        new_automation.states.append(vertex)
        for edge in one_letter_transmissions:
            if edge.from_ == vertex:
                dfs_for_states(edge.to_)

    dfs_for_states(new_automation.start)
    for transmission in one_letter_transmissions:
        if transmission.from_ in new_automation.states:
            new_automation.transmissions.append(transmission)

    def path_to_finish_by_empty_transmissions(vertex):
        if vertex == automation.finish:
            return True
        for edge in automation.transmissions:
            if edge.from_ == vertex and edge.by == '':
                if path_to_finish_by_empty_transmissions(edge.to_):
                    return True

        return False

    new_automation.finishes = []
    for state in new_automation.states:
        if path_to_finish_by_empty_transmissions(state):
            new_automation.finishes.append(state)

    return new_automation


def max_possible_suffix(word: str, automation: FiniteAutomation) -> int:
    states_from_previous_suffix = set(automation.finishes)
    result = 0
    for symbol in reversed(word):
        states_for_this_suffix = set()
        for state in states_from_previous_suffix:
            for transmission in automation.transmissions:
                if transmission.to_ == state and transmission.by == symbol:
                    states_for_this_suffix.add(transmission.from_)
        if len(states_for_this_suffix) == 0:
            break
        else:
            result += 1
            states_from_previous_suffix = states_for_this_suffix
    return result

a = "acb..bab.c.*.ab.ba.+.+*a"

b = remove_empty_transmissions(automation_from_expression(a))

print(max_possible_suffix("cbaa", b))
