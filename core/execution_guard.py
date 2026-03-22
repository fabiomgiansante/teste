from contextlib import contextmanager

import streamlit as st


class SessionExecutionGuard:
    def __init__(self, key: str) -> None:
        self._state_key = f"_running_{key}"

    def is_running(self) -> bool:
        return bool(st.session_state.get(self._state_key, False))

    @contextmanager
    def running(self):
        if self.is_running():
            raise RuntimeError("Ja existe uma execucao em andamento para esta tarefa.")

        st.session_state[self._state_key] = True
        try:
            yield
        finally:
            st.session_state[self._state_key] = False
