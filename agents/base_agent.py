"""
Base Agent Class for Security System
All security agents inherit from this class.
"""

import threading
import time
from datetime import datetime
from typing import Dict, Any, List


class BaseSecurityAgent:
    """Base class for all security agents."""

    def __init__(self, name: str, agent_type: str):
        """
        Initialize a security agent.

        Args:
            name: Agent's name
            agent_type: Type of agent (watcher, scanner, alert, coordinator)
        """
        self.name = name
        self.agent_type = agent_type
        self.active = False
        self.memory = []
        self.log = []
        self.coordinator = None
        self.thread = None

    def start(self):
        """Start the agent in a separate thread."""
        if not self.active:
            self.active = True
            self.thread = threading.Thread(target=self.run, daemon=True)
            self.thread.start()
            self.log_action("STARTED", f"{self.name} is now active")

    def stop(self):
        """Stop the agent."""
        self.active = False
        if self.thread:
            self.thread.join(timeout=5)
        self.log_action("STOPPED", f"{self.name} has been stopped")

    def run(self):
        """
        Main agent loop - override in child classes.
        This method runs continuously while agent is active.
        """
        raise NotImplementedError("Agents must implement run() method")

    def perceive(self, environment_state: Dict[str, Any]) -> Dict[str, Any]:
        """
        Perceive and filter environment state.

        Args:
            environment_state: Current state of the environment

        Returns:
            Filtered perception relevant to this agent
        """
        return environment_state

    def decide(self, perception: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a decision based on perception.

        Args:
            perception: Agent's perception of the environment

        Returns:
            Decision dict with 'action' and 'reasoning'
        """
        raise NotImplementedError("Agents must implement decide() method")

    def act(self, decision: Dict[str, Any]) -> Any:
        """
        Execute the decision.

        Args:
            decision: The decision to execute

        Returns:
            Result of the action
        """
        action = decision.get('action')
        reasoning = decision.get('reasoning', 'No reasoning provided')

        # Log the action
        self.log_action(action, reasoning)

        # Store in memory
        self.memory.append({
            'timestamp': datetime.now(),
            'action': action,
            'reasoning': reasoning
        })

        return decision

    def report_to_coordinator(self, event: Dict[str, Any]):
        """
        Report an event to the coordinator agent.

        Args:
            event: Event data to report
        """
        if self.coordinator:
            self.coordinator.receive_report(self.name, event)

    def log_action(self, action: str, details: str):
        """
        Log an action for monitoring and debugging.

        Args:
            action: Type of action
            details: Action details
        """
        log_entry = {
            'timestamp': datetime.now(),
            'agent': self.name,
            'action': action,
            'details': details
        }
        self.log.append(log_entry)

    def get_status(self) -> Dict[str, Any]:
        """
        Get current agent status.

        Returns:
            Status dict with agent information
        """
        return {
            'name': self.name,
            'type': self.agent_type,
            'active': self.active,
            'actions_taken': len(self.memory),
            'last_action': self.memory[-1] if self.memory else None
        }

    def get_recent_logs(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent log entries.

        Args:
            limit: Maximum number of entries to return

        Returns:
            List of recent log entries
        """
        return self.log[-limit:]
