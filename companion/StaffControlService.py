"""Validated commands for reversible private test actors; no save-roster editing."""
import json
import math
from pathlib import Path
import threading
import time
import uuid

LIMIT = 10

class StaffCommandError(ValueError):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.status = status

class StaffControlService:
    def __init__(self, mod):
        self.mod = Path(mod)
        self.lock = threading.Lock()
        self.cache = None
        self.updated = None
        self.pending_id = None
        self.pending_until = 0

    def snapshot(self):
        try:
            path = self.mod / 'nlab_staff_control_status.json'
            value = json.loads(path.read_bytes())
            if isinstance(value, dict) and value.get('schema') == 1:
                self.cache, self.updated = value, path.stat().st_mtime
        except (OSError, ValueError):
            pass
        if self.cache is None:
            return {'schema': 1, 'ready': False, 'limit': LIMIT, 'loaded': 0, 'free': 0,
                    'managedCount': 0, 'activeCount': 0, 'initializing': 0,
                    'feedAgeSeconds': None, 'unavailable': 'Test staff controller has not reported yet'}
        return {**self.cache, 'feedAgeSeconds': max(0, time.time() - self.updated)}

    @staticmethod
    def validate(payload):
        if not isinstance(payload, dict) or set(payload) != {'action', 'count'}:
            raise StaffCommandError('Expected an action and count')
        action, count = payload['action'], payload['count']
        if not isinstance(action, str) or action not in {'add', 'remove', 'count', 'clear'}:
            raise StaffCommandError('Unsupported staff action')
        if type(count) is not int or not 0 <= count <= LIMIT:
            raise StaffCommandError('Count must be an integer from 0 to 10')
        if action in {'add', 'remove'} and count == 0:
            raise StaffCommandError('Add/remove amount must be at least one')
        if action == 'clear' and count != 0:
            raise StaffCommandError('Clear requires count zero')
        return action, count

    def submit(self, payload, runtime_ready):
        action, count = self.validate(payload)
        with self.lock:
            state = self.snapshot()
            age = state.get('feedAgeSeconds')
            if (not runtime_ready or not state.get('ready') or state.get('mission') != 30050
                    or not isinstance(age, (int, float)) or not math.isfinite(age) or age > 10):
                raise StaffCommandError('Open the normal Mother Base Command platform to use test staff controls', 409)
            if self.pending_id and state.get('lastCommand') != self.pending_id and time.monotonic() < self.pending_until:
                raise StaffCommandError('The previous staff command is still waiting for the game', 409)
            current, free = state.get('managedCount', 0), state.get('free', 0)
            target = count if action == 'count' else (0 if action == 'clear'
                     else max(0, current + (count if action == 'add' else -count)))
            if target > LIMIT:
                raise StaffCommandError('The private test pool supports at most ten soldiers', 409)
            if target > current + free:
                raise StaffCommandError('There are not enough free loaded test slots', 409)
            uid = 'staff_' + uuid.uuid4().hex[:12]
            path = self.mod / 'nlab_staff_command.txt'
            temporary = path.with_name(path.name + '.' + uid + '.tmp')
            temporary.write_text(f'{uid} {action} {count}\n', encoding='utf-8', newline='\n')
            temporary.replace(path)
            self.pending_id, self.pending_until = uid, time.monotonic() + 15
            return {'id': uid, 'action': action, 'count': count, 'target': target,
                    'message': 'Queued for the game; active count updates after physical initialization'}
