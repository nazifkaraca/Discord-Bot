{ pkgs }: {
  deps = [
    pkgs.python39Full
    pkgs.ffmpeg
    pkgs.yt-dlp
    pkgs.python39Packages.pytube
  ];

  # Optionally, you can include a shellHook to install any additional Python packages from requirements.txt
  shellHook = ''
    export PATH=$PATH:./.venv/bin
    pip install -r requirements.txt
  '';
}
