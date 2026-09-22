"""A tiny to-do list using a data model (dataclasses)."""

from dataclasses import dataclass, field, asdict
from datetime import date
import json


@dataclass
class Task:
    """One to-do item — the blueprint for each task."""
    title: str
    done: bool = False
    due: date | None = None

    def mark_done(self):
        self.done = True


@dataclass
class TodoList:
    """A whole list of tasks."""
    name: str
    tasks: list[Task] = field(default_factory=list)

    def add(self, title: str, due: date | None = None):
        task = Task(title=title, due=due)
        self.tasks.append(task)
        return task

    def pending(self) -> list[Task]:
        return [t for t in self.tasks if not t.done]

    def save(self, path: str):
        """Save the list as JSON (convert dataclasses -> dicts)."""
        with open(path, "w") as f:
            json.dump(asdict(self), f, indent=2, default=str)

    @classmethod
    def load(cls, path: str, default_name: str = "My Week"):
        """Load the list from JSON, or start fresh if the file doesn't exist yet."""
        try:
            with open(path) as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return cls(default_name)

        todos = cls(data.get("name", default_name))
        for t in data.get("tasks", []):
            due = date.fromisoformat(t["due"]) if t.get("due") else None
            task = Task(title=t["title"], done=t.get("done", False), due=due)
            todos.tasks.append(task)
        return todos

    def __str__(self):
        lines = [f"📋 {self.name}"]
        for i, t in enumerate(self.tasks, 1):
            mark = "✅" if t.done else "⬜"
            lines.append(f"  {i}. {mark} {t.title} (due: {t.due})")
        return "\n".join(lines)


if __name__ == "__main__":
    todos = TodoList("My Week")
    todos.add("Buy milk", due=date(2026, 9, 18))
    todos.add("Finish data model notes")
    todos.add("Call grandma", due=date(2026, 9, 20))

    todos.tasks[1].mark_done()

    print(todos)
    print(f"\nPending: {len(todos.pending())} task(s)")

    todos.save("todos.json")
    print("\nSaved to todos.json ✔")
