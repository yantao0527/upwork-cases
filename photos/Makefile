
srv-photos:
	python photos.py

srv-download:
	python download.py

download-A:
	curl http://127.0.0.1:2200/download-folder?folder_name=FolderA

download-E:
	# curl "http://127.0.0.1:2200/download-folder?folder_name=Folder%20E"
	curl "http://127.0.0.1:2200/download-folder?folder_name=Folder%20E&extension=pdf&extension=png&extension=jpg"

download-sub:
	curl "http://127.0.0.1:2200/download-folder?folder_name=Folder%20E/sub"