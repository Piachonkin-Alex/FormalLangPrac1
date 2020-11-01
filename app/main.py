from types import SimpleNamespace

FiniteAutomation = SimpleNamespace  # Everything is a SimpleNamespace
Transmission = SimpleNamespace


def automation_from_expression(expression: str) -> FiniteAutomation:
    next_state_name = 0  # counter for number of all states
    stack_of_automation = []  # stack for reverse polish notation
    for symbol in expression:
        if symbol == '.':  # concat
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
            concat_automation.transmissions.append(bridge)  # add bridge from left.finish to right.start
            stack_of_automation.append(concat_automation)  # return on stack
        elif symbol == '+':  # sum
            right_expr = stack_of_automation.pop()
            left_expr = stack_of_automation.pop()
            sum_automation = FiniteAutomation()
            sum_automation.states = left_expr.states
            sum_automation.states += right_expr.states
            sum_automation.states.append(next_state_name)
            sum_automation.states.append(next_state_name + 1)
            sum_automation.start = next_state_name  # new start
            sum_automation.finish = next_state_name + 1  # new finish
            sum_automation.transmissions = left_expr.transmissions
            sum_automation.transmissions += right_expr.transmissions
            from_start_to_left = Transmission(
                from_=next_state_name,
                to_=left_expr.start,
                by=''
            )
            sum_automation.transmissions.append(from_start_to_left)  # start -> left.start
            from_start_to_right = Transmission(
                from_=next_state_name,
                to_=right_expr.start,
                by=''
            )
            sum_automation.transmissions.append(from_start_to_right)  # start -> right.start
            from_left_to_end = Transmission(
                from_=left_expr.finish,
                to_=next_state_name + 1,
                by=''
            )
            sum_automation.transmissions.append(from_left_to_end)  # left.finish -> finish
            from_right_to_end = Transmission(
                from_=right_expr.finish,
                to_=next_state_name + 1,
                by=''
            )
            sum_automation.transmissions.append(from_right_to_end)  # right.finish -> finish
            stack_of_automation.append(sum_automation)  # return on stack
            next_state_name += 2  # update counter
        elif symbol == "1":  # empty
            empty_automation = FiniteAutomation()
            empty_automation.states = [next_state_name]  # one state
            empty_automation.start = next_state_name
            empty_automation.finish = next_state_name
            empty_automation.transmissions = []  # no transmissions
            next_state_name += 1
            stack_of_automation.append(empty_automation)  # add on stack
        elif symbol == "*":
            edit_automation = stack_of_automation.pop()
            if edit_automation.start == edit_automation.finish:  # check is it stared before (ex. 1*, (a*)* )
                stack_of_automation.append(edit_automation)
                continue
            finish_to_start_edge = Transmission(
                from_=edit_automation.finish,
                to_=edit_automation.start,
                by=''
            )
            edit_automation.transmissions.append(finish_to_start_edge)  # finish -> start
            edit_automation.finish = edit_automation.start  # finish = start
            stack_of_automation.append(edit_automation)  # return in stack
        else:
            base_automation = FiniteAutomation()
            base_automation.states = [next_state_name, next_state_name + 1]  # 2 states
            base_automation.start = next_state_name
            base_automation.finish = next_state_name + 1
            edge = Transmission(
                from_=next_state_name,
                to_=next_state_name + 1,
                by=symbol
            )
            base_automation.transmissions = [edge]  # 1 edge: start -> finish by letter
            next_state_name += 2  # update counter
            stack_of_automation.append(base_automation)  # add on stack
    return stack_of_automation.pop()


def remove_empty_transmissions(automation: FiniteAutomation) -> FiniteAutomation:
    new_automation = FiniteAutomation()
    new_automation.transmissions = []
    one_letter_transmissions = []

    def dfs_for_one_letter_transmissions(start_state, cur_state):
        for edge in automation.transmissions:
            if edge.from_ == cur_state:
                if edge.by != '':  # we found an nonempty edge from start_state to edge.to_
                    new_transmission = Transmission(
                        from_=start_state,
                        to_=edge.to_,
                        by=edge.by
                    )
                    one_letter_transmissions.append(new_transmission)
                else:  # continue recursion
                    dfs_for_one_letter_transmissions(start_state, edge.to_)

    for state in automation.states:
        dfs_for_one_letter_transmissions(state, state)

    new_automation.start = automation.start
    new_automation.states = []

    def dfs_for_states(vertex):  # find all reachable states for state vertex
        if vertex in new_automation.states:
            return
        new_automation.states.append(vertex)
        for edge in one_letter_transmissions:
            if edge.from_ == vertex:
                dfs_for_states(edge.to_)

    dfs_for_states(new_automation.start)  # all reachable states for start
    for transmission in one_letter_transmissions:  # remove extra copies
        if transmission.from_ in new_automation.states:
            new_automation.transmissions.append(transmission)

    def path_to_finish_by_empty_transmissions(vertex):  # try to find empty path from vertex to finish
        if vertex == automation.finish:
            return True
        for edge in automation.transmissions:
            if edge.from_ == vertex and edge.by == '':
                if path_to_finish_by_empty_transmissions(edge.to_):
                    return True

        return False

    new_automation.finishes = []
    for state in new_automation.states:  # find all new finishes
        if path_to_finish_by_empty_transmissions(state):
            new_automation.finishes.append(state)

    return new_automation


def max_possible_suffix(word: str, automation: FiniteAutomation) -> int:
    states_from_previous_suffix = set(automation.finishes)  # possible states for previous suffix
    result = 0  # the max length of suffix
    for symbol in reversed(word):
        states_for_this_suffix = set()  # possible states for current suffix
        for state in states_from_previous_suffix:
            for transmission in automation.transmissions:  # try to find possible states for current suffix
                if transmission.to_ == state and transmission.by == symbol:
                    states_for_this_suffix.add(transmission.from_)
        if len(states_for_this_suffix) == 0:  # no state for this suffix -- return result
            break
        else:
            result += 1  # update result
            states_from_previous_suffix = states_for_this_suffix

    return result


def max_possible_suffix_of_expr(expression: str, word: str):
    one_letter_automation = remove_empty_transmissions(automation_from_expression(expression))
    return max_possible_suffix(word, one_letter_automation)


if __name__ == '__main__':
    expr1 = 'ab+c.aba.*.bac.+.+*'
    expr2 = 'acb..bab.c.*.ab.ba.+.+*a.'
    word1 = 'babc'
    word2 = 'cbaa'
    assert (max_possible_suffix_of_expr(expr1, word1) == 2)
    assert (max_possible_suffix_of_expr(expr2, word2) == 4)
