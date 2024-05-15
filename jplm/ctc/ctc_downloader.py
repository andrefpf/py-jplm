import os
import shutil
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass
from pathlib import Path
from time import time
from zipfile import BadZipFile, ZipFile

import requests

URL_TEMPLATE = "http://plenodb.jpeg.org/lf/pleno_lf/{name}.zip"
COMMAND_SHIFT_TEMPLATE = (
    "{jplm_bin}/utils/lenslet_13x13_shifter -i {input_path}/ -o {output_path}/"
)
COMMAND_CONVERT_TEMPLATE = (
    "{jplm_bin}/utils/convert_ppm_to_pgx -i {input_path} -o {output_path}/"
)


class CTCDownloader:
    def __init__(self, jplm_bin_path=None):
        if jplm_bin_path is not None:
            self.jplm_bin_path = jplm_bin_path
        elif "JPLM_BIN" in os.environ:
            self.jplm_bin_path = os.environ["JPLM_BIN"]
        else:
            raise ValueError(
                "JPLM binary folder not found.\n"
                "\tYou can provide a path through the ambient variable JPLM_BIN"
            )

    def download_all_ctc(self, path, remove_tmp=True):
        light_fields = [
            "Bikes",
            "Danger_de_Mort",
            "Fountain_Vincent2",
            "Stone_Pillars_Outside",
            "greek",
            "sideboard",
            "poznanlab1",
            "set2",
            "tarot",
        ]
        self.download_multiple_lfs(light_fields, path, remove_tmp)

    def download_all_lenslets(self, path, remove_tmp=True):
        light_fields = [
            "Bikes",
            "Danger_de_Mort",
            "Fountain_Vincent2",
            "Stone_Pillars_Outside",
        ]
        self.download_multiple_lfs(light_fields, path, remove_tmp)

    def download_all_non_lenslet(self, path, remove_tmp=True):
        light_fields = ["greek", "sideboard", "poznanlab1", "set2", "tarot"]
        self.download_multiple_lfs(light_fields, path, remove_tmp)

    def download_multiple_lfs(self, names, target_path, remove_tmp=True):
        target_path = Path(target_path)

        with ThreadPoolExecutor() as executor:
            futures = []
            for name in names:
                url = URL_TEMPLATE.format(name=name)
                zipped_path = Path(target_path) / f".zipped/{name}.zip"
                zipped_path.parent.mkdir(exist_ok=True, parents=True)

                print(f"Downloading {name}")
                submition = executor.submit(self._download_zip, url, zipped_path)
                futures.append(submition)

            for future in as_completed(futures):
                future.result()

        lenslets = [
            "Bikes",
            "Danger_de_Mort",
            "Fountain_Vincent2",
            "Stone_Pillars_Outside",
        ]
        for name in names:
            zipped_path = Path(target_path) / f".zipped/{name}.zip"
            ppm_path = Path(target_path) / f".ppm/{name}/"
            pgx_path = Path(target_path) / f".pgx/{name}/"
            final_path = Path(target_path) / f"{name}/"

            ppm_path.mkdir(exist_ok=True, parents=True)
            pgx_path.mkdir(exist_ok=True, parents=True)
            final_path.mkdir(exist_ok=True, parents=True)

            print(f"Unzipping {name}")
            try:
                self._unzip_file(zipped_path, ppm_path)
            except BadZipFile as error:
                print(f"Failed to download {name}")
                print(error)
                continue

            if name in lenslets:
                print(f"Converting {name} to pgx")
                self._convert_to_pgx(ppm_path, pgx_path)

                print(f"Shifting {name}")
                self._shift_views(pgx_path, final_path)

            else:
                print(f"Converting {name} to pgx")
                self._convert_to_pgx(ppm_path, final_path)

        if remove_tmp:
            print(f"Removing temporary files for {name}")
            shutil.rmtree(target_path / ".zipped")
            shutil.rmtree(target_path / ".ppm")
            shutil.rmtree(target_path / ".pgx")

        print(f"Finished {name}")

    def download_lf(self, name, target_path, remove_tmp=True):
        url = URL_TEMPLATE.format(name=name)
        zipped_path = Path(target_path) / f".zipped/{name}.zip"
        ppm_path = Path(target_path) / f".ppm/{name}/"
        pgx_path = Path(target_path) / f".pgx/{name}/"
        final_path = Path(target_path) / f"{name}/"

        zipped_path.parent.mkdir(exist_ok=True, parents=True)
        ppm_path.mkdir(exist_ok=True, parents=True)
        pgx_path.mkdir(exist_ok=True, parents=True)
        final_path.mkdir(exist_ok=True, parents=True)

        print(f"Downloading {name}")
        self._download_zip(url, zipped_path)

        print(f"Unzipping {name}")
        try:
            self._unzip_file(zipped_path, ppm_path)
        except BadZipFile as error:
            print(f"Failed to download {name}")
            print(error)
            return

        lenslets = [
            "Bikes",
            "Danger_de_Mort",
            "Fountain_Vincent2",
            "Stone_Pillars_Outside",
        ]
        if name in lenslets:
            print(f"Converting {name} to pgx")
            self._convert_to_pgx(ppm_path, pgx_path)

            print(f"Shifting {name}")
            self._shift_views(pgx_path, final_path)

        else:
            print(f"Converting {name} to pgx")
            self._convert_to_pgx(ppm_path, final_path)

        if remove_tmp:
            print(f"Removing temporary files for {name}")
            shutil.rmtree(zipped_path.parent)
            shutil.rmtree(ppm_path)
            shutil.rmtree(pgx_path)

        print(f"Finished {name}")

    def _download_zip(self, url, target_path):
        with requests.get(url, stream=True) as request:
            with open(target_path, "wb") as file:
                shutil.copyfileobj(request.raw, file)

    def _unzip_file(self, origin_path, target_path):
        with ZipFile(origin_path, "r") as zip_ref:
            zip_ref.extractall(target_path)

    def _convert_to_pgx(self, origin_path, target_path):
        origin_path = Path(origin_path)
        target_path = Path(target_path)

        origin_path.mkdir(exist_ok=True, parents=True)
        target_path.mkdir(exist_ok=True, parents=True)

        pathlist = Path(origin_path).glob("*.ppm")
        for path in pathlist:
            command = COMMAND_CONVERT_TEMPLATE.format(
                jplm_bin=self.jplm_bin_path,
                input_path=path.resolve(),
                output_path=target_path.resolve(),
            ).split()

            res = subprocess.run(command, capture_output=True)
            if res.returncode != 0:
                raise Exception(res.stderr)

    def _shift_views(self, origin_path, target_path):
        origin_path = Path(origin_path)
        target_path = Path(target_path)

        origin_path.mkdir(exist_ok=True, parents=True)
        target_path.mkdir(exist_ok=True, parents=True)

        command = COMMAND_SHIFT_TEMPLATE.format(
            jplm_bin=self.jplm_bin_path,
            input_path=origin_path.resolve(),
            output_path=target_path.resolve(),
        ).split()

        res = subprocess.run(command, capture_output=True)
        if res.returncode != 0:
            raise Exception(res.stderr)
