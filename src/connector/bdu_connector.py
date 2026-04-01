import sys
import time
from typing import Optional
from datetime import datetime, timedelta, timezone

from pycti import OpenCTIConnectorHelper  # type: ignore
from src import ConfigLoader
from src.services import BDUConverter  # type: ignore


class BDUConnector:
    def __init__(self):
        """
        Initialize the BDUConnector with necessary configurations
        """

        # Load configuration file and connection helper
        # Instantiate the connector helper from config
        self.config = ConfigLoader()
        self.helper = OpenCTIConnectorHelper(config=self.config.model_dump_pycti())
        self.converter = BDUConverter(self.helper, self.config)

    def run(self) -> None:
        """
        Main execution loop procedure for BDU Connector
        """
        self.helper.connector_logger.info("[CONNECTOR] Fetching datasets...")
        get_run_and_terminate = getattr(self.helper, "get_run_and_terminate", None)
        if callable(get_run_and_terminate) and self.helper.get_run_and_terminate():
            self.process_data()
            self.helper.force_ping()
        else:
            while True:
                self.process_data()
                time.sleep(60)

    def _initiate_work(self, timestamp: int) -> Optional[str | None]:
        """
        Initialize a work
        :param timestamp: Timestamp in integer
        :return: Work id in string
        """
        now = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        friendly_name = f"{self.helper.connect_name} run @ " + now.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        work_id = self.helper.api.work.initiate_work(
            self.helper.connect_id, friendly_name
        )

        info_msg = f"[CONNECTOR] New work '{work_id}' initiated..."
        self.helper.connector_logger.info(info_msg)

        return work_id

    def update_connector_state(self, current_time: int, work_id: str) -> None:
        """
        Update the connector state
        :param current_time: Time in int
        :param work_id: Work id in string
        """
        msg = (
            f"[CONNECTOR] Connector successfully run, storing last_run as "
            f"{datetime.fromtimestamp(current_time, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}"
        )
        self.helper.connector_logger.info(msg)
        self.helper.api.work.to_processed(work_id, msg)
        self.helper.set_state({"last_run": current_time})

        interval_in_hours = round(self.interval / 60 / 60, 2)
        self.helper.connector_logger.info(
            "[CONNECTOR] Last_run stored, next run in: "
            + str(interval_in_hours)
            + " hours"
        )

    def process_data(self) -> None:
        try:
            """
            Get the current state and check if connector already runs
            """
            now = datetime.now()
            current_time: int = int(datetime.timestamp(now))
            current_state = self.helper.get_state()
            last_run: int = 0

            if current_state is not None and "last_run" in current_state:
                last_run: int = current_state["last_run"]

                msg = "[CONNECTOR] Connector last run: " + datetime.fromtimestamp(
                    last_run, tz=timezone.utc
                ).strftime("%Y-%m-%d %H:%M:%S")
                self.helper.connector_logger.info(msg)
            else:
                msg = "[CONNECTOR] Connector has never run..."
                self.helper.connector_logger.info(msg)

            """
            ======================================================
            Main process if connector successfully works
            ======================================================
            """
            # TODO: rewrite logic of running
            if (current_time - last_run) >= int(self.interval):
                # Initiate work_id to track the job
                work_id = self._initiate_work(current_time)
                self.converter.send_bundle(last_run, work_id)
                self.update_connector_state(current_time, work_id)

            else:
                new_interval = self.interval - (current_time - last_run)
                new_interval_in_hours = round(new_interval / 60 / 60, 2)
                self.helper.connector_logger.info(
                    "[CONNECTOR] Connector will not run, next run in: "
                    + str(new_interval_in_hours)
                    + " hours"
                )

            time.sleep(5)

        except (KeyboardInterrupt, SystemExit):
            msg = "[CONNECTOR] Connector stop..."
            self.helper.connector_logger.info(msg)
            sys.exit(0)
        except Exception as e:
            error_msg = f"[CONNECTOR] Error while processing data: {str(e)}"
            self.helper.connector_logger.error(error_msg, meta={"error": str(e)})
