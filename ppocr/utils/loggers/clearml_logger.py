from .base_logger import BaseLogger


class ClearMLLogger(BaseLogger):
    def __init__(self, project_name, task_name, save_dir):
        try:
            from clearml import Task, Logger
        except ModuleNotFoundError:
            raise ModuleNotFoundError(
                "Please install clearml using `pip install clearml`"
            )
        super().__init__(save_dir)
        self.task: Task = Task.init(project_name=project_name, task_name=task_name)
        self.clearml_logger = Logger.current_logger()

    def log_metrics(self, metrics, prefix=None, step=None):
        if not prefix:
            prefix = ""

        for k, v in metrics.items():
            self.clearml_logger.report_scalar(
                title=prefix, series=k, value=v, iteration=step
            )

    def log_model(self, is_best, prefix, metadata=None):
        pass

    def close(self):
        self.task.close()
