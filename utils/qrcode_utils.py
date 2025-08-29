from io import BytesIO
import qrcode

def to_qr_code(original_url: str, file_path: str = "qrcode.png") -> str:
	qr = qrcode.QRCode(
		version=1,
		error_correction=qrcode.constants.ERROR_CORRECT_L,
		box_size=10,
		border=4,
	)
	qr.add_data(original_url)
	qr.make(fit=True)

	img = qr.make_image(fill_color="black", back_color="white")
	if file_path:
		img.save(file_path)
	# If file_path is a relative path (e.g., "qrcode.png"), the file is saved to the current working directory.
	# If file_path is an absolute path (e.g., "/home/lydia/project/static/qrcode.png", start with "/"), the file is saved there directly.

	else:
		# if json request has file_path=None
		buffer = BytesIO()
		img.save(buffer, format="PNG")
		buffer.seek(0)
		return buffer
	return file_path
