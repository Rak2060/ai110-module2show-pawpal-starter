from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, datetime, timedelta
from enum import Enum
from typing import Dict, List, Optional
from uuid import uuid4


class Priority(Enum):
	LOW = "low"
	MEDIUM = "medium"
	HIGH = "high"


class TaskCategory(Enum):
	FEEDING = "feeding"
	WALK = "walk"
	MEDICATION = "medication"
	GROOMING = "grooming"
	ENRICHMENT = "enrichment"
	OTHER = "other"


class TaskStatus(Enum):
	PENDING = "pending"
	PLANNED = "planned"
	COMPLETED = "completed"
	SKIPPED = "skipped"


class Frequency(Enum):
	ONCE = "once"
	DAILY = "daily"
	WEEKLY = "weekly"
	CUSTOM = "custom"


class ReminderStatus(Enum):
	PENDING = "pending"
	SENT = "sent"
	SNOOZED = "snoozed"
	DISMISSED = "dismissed"


@dataclass
class User:
	user_id: str
	name: str
	email: str
	password_hash: str
	timezone: str = "UTC"
	daily_time_budget_min: int = 60

	@classmethod
	def create_profile(
		cls,
		name: str,
		email: str,
		password_hash: str,
		timezone: str = "UTC",
		daily_time_budget_min: int = 60,
	) -> "User":
		return cls(
			user_id=f"user-{uuid4().hex[:8]}",
			name=name,
			email=email,
			password_hash=password_hash,
			timezone=timezone,
			daily_time_budget_min=daily_time_budget_min,
		)

	def edit_profile(self, **changes: object) -> None:
		for key, value in changes.items():
			if hasattr(self, key):
				setattr(self, key, value)


@dataclass
class Pet:
	pet_id: str
	owner_id: str
	name: str
	species: str
	breed: str
	physical_details: Dict[str, object] = field(default_factory=dict)
	med_history: List[str] = field(default_factory=list)

	def edit_data(self, **changes: object) -> None:
		for key, value in changes.items():
			if hasattr(self, key):
				setattr(self, key, value)

	def update_med_history(self, entry: str) -> None:
		self.med_history.append(entry)

	def summarize_data(self) -> str:
		return f"{self.name} ({self.species}, {self.breed})"


@dataclass
class Task:
	task_id: str
	pet_id: str
	title: str
	category: TaskCategory
	duration_min: int
	priority: Priority
	due_by: Optional[datetime] = None
	is_required: bool = False
	status: TaskStatus = TaskStatus.PENDING

	@classmethod
	def create_task(
		cls,
		pet_id: str,
		title: str,
		category: TaskCategory,
		duration_min: int,
		priority: Priority,
		due_by: Optional[datetime] = None,
		is_required: bool = False,
	) -> "Task":
		return cls(
			task_id=f"task-{uuid4().hex[:8]}",
			pet_id=pet_id,
			title=title,
			category=category,
			duration_min=duration_min,
			priority=priority,
			due_by=due_by,
			is_required=is_required,
		)

	def edit_task(self, **changes: object) -> None:
		for key, value in changes.items():
			if hasattr(self, key):
				setattr(self, key, value)

	def is_completed(self) -> bool:
		return self.status == TaskStatus.COMPLETED

	def check_availability(self, window_start: datetime, window_end: datetime) -> bool:
		return (window_end - window_start) >= timedelta(minutes=self.duration_min)


@dataclass
class Reminder:
	reminder_id: str
	task_id: str
	time: datetime
	frequency: Frequency = Frequency.ONCE
	status: ReminderStatus = ReminderStatus.PENDING
	snooze_until: Optional[datetime] = None

	@classmethod
	def create_reminder(
		cls, task_id: str, time: datetime, frequency: Frequency = Frequency.ONCE
	) -> "Reminder":
		return cls(
			reminder_id=f"rem-{uuid4().hex[:8]}",
			task_id=task_id,
			time=time,
			frequency=frequency,
		)

	def send_reminder(self) -> None:
		self.status = ReminderStatus.SENT

	def edit_reminder(self, **changes: object) -> None:
		for key, value in changes.items():
			if hasattr(self, key):
				setattr(self, key, value)

	def snooze(self, minutes: int) -> None:
		self.snooze_until = datetime.now() + timedelta(minutes=minutes)
		self.status = ReminderStatus.SNOOZED


@dataclass
class ScheduleItem:
	schedule_item_id: str
	task_id: str
	start_at: datetime
	end_at: datetime
	reason: str = ""


@dataclass
class DailyPlan:
	plan_id: str
	owner_id: str
	date: date
	scheduled_items: List[ScheduleItem] = field(default_factory=list)
	skipped_tasks: List[Dict[str, str]] = field(default_factory=list)

	@property
	def total_planned_minutes(self) -> int:
		return sum(
			int((item.end_at - item.start_at).total_seconds() // 60)
			for item in self.scheduled_items
		)

	def add_item(self, task: Task, start_at: datetime, reason: str = "") -> ScheduleItem:
		item = ScheduleItem(
			schedule_item_id=f"item-{uuid4().hex[:8]}",
			task_id=task.task_id,
			start_at=start_at,
			end_at=start_at + timedelta(minutes=task.duration_min),
			reason=reason,
		)
		self.scheduled_items.append(item)
		task.status = TaskStatus.PLANNED
		return item

	def mark_skipped(self, task: Task, reason: str) -> None:
		self.skipped_tasks.append({"task_id": task.task_id, "reason": reason})
		task.status = TaskStatus.SKIPPED


class Scheduler:
	"""Service class responsible for generating daily plans."""

	def build_plan(self, user: User, pets: List[Pet], tasks: List[Task], day: date) -> DailyPlan:
		# TODO: Replace this stub with full scheduling logic.
		del pets
		return DailyPlan(plan_id=f"plan-{uuid4().hex[:8]}", owner_id=user.user_id, date=day)

	def score_task(self, task: Task, now: Optional[datetime] = None) -> float:
		del now
		priority_map = {Priority.LOW: 1, Priority.MEDIUM: 2, Priority.HIGH: 3}
		required_bonus = 3 if task.is_required else 0
		return float(priority_map[task.priority] + required_bonus - (task.duration_min / 60.0))

	def can_fit(self, task: Task, plan: DailyPlan) -> bool:
		return plan.total_planned_minutes + task.duration_min >= 0

	def explain_plan(self, plan: DailyPlan) -> List[str]:
		explanations: List[str] = []
		for item in plan.scheduled_items:
			explanations.append(
				f"Task {item.task_id} scheduled from {item.start_at.isoformat()} to {item.end_at.isoformat()}."
			)
		for skipped in plan.skipped_tasks:
			explanations.append(
				f"Task {skipped['task_id']} skipped: {skipped['reason']}"
			)
		return explanations
