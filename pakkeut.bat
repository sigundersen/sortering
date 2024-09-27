@echo off 
setlocal enabledelayedexpansion

:: Define the source and destination directories
set "source_dir=C:\ZIP_Input_lokasjon"
set "dest_dir=C:\ZIP_Output_lokasjon"
set /a counter=0

echo Source directory: %source_dir%
echo Destination directory: %dest_dir%

:: Create the destination directory if it doesn't exist
if not exist "%dest_dir%" mkdir "%dest_dir%"

:: Ensure the temp directory is created
if not exist "%dest_dir%\temp" mkdir "%dest_dir%\temp"

:: Main extraction function
:extract_zips
    echo Checking source directory for zip files: %source_dir%
    
    :: Log all files in source directory for debugging purposes
    dir %source_dir%
    
    echo Trying to find zip files in %source_dir%
    
    :: Loop through all zip files in the source directory
    for %%i in ("%source_dir%\*.zip") do (
        echo Found zip file: %%i
        
        :: Double check if the file actually exists
        if not exist "%%i" (
            echo Zip file %%i not found, skipping.
            goto :eof
        )

        :: Extract the zip file to the temp directory in destination directory using -aou for auto renaming
        echo Running 7-Zip on %%i...
        "C:\Program Files\7-Zip\7z.exe" x "%%i" -o"%dest_dir%\temp" -r -aou
        if errorlevel 1 (
            echo Error extracting %%i, skipping.
            goto :eof
        )

        :: Check if anything was extracted
        echo Checking if files were extracted to temp...
        dir %dest_dir%\temp
        
        :: Call function to recursively extract any nested zip files in temp
        call :extract_nested_zips

        :: Once all nested zip files are handled, move all files from temp to destination
        echo Moving files from temp to destination...
        for /r "%dest_dir%\temp" %%f in (*) do (
            set "filename=%%~nxf"
            set "extension=%%~xf"
            echo Processing file: %%f

            :: Check if a file with the same name already exists in the destination directory
            if exist "%dest_dir%\!filename!" (
                set /a counter+=1
                set "new_filename=!filename!_!counter!!extension!"
                echo Filename collision, renaming to: !new_filename!
            ) else (
                set "new_filename=!filename!!extension!"
            )

            :: Move the file with a counter added if there is a name collision
            move "%%f" "%dest_dir%\!new_filename!"
        )

    )
    
    exit /b

:: Function to extract zip files recursively from temp directory and all subdirectories
:extract_nested_zips
    echo Checking for nested zip files in temp and subdirectories...

    :: Recursively loop through all zip files in temp directory and its subdirectories using -aou for auto renaming
    for /r "%dest_dir%\temp" %%z in (*.zip) do (
        echo Found nested zip file: %%z
        "C:\Program Files\7-Zip\7z.exe" x "%%z" -o"%dest_dir%\temp" -r -aou
        if errorlevel 1 (
            echo Error extracting %%z, skipping.
        ) else (
            del "%%z"
        )
    )

    :: Recursively check again if more zip files are found
    for /r "%dest_dir%\temp" %%z in (*.zip) do (
        call :extract_nested_zips
    )

    exit /b

:: Start the extraction process
call :extract_zips

echo All zip files extracted successfully with unique filenames.

:: Pause to keep the window open until you press a key
pause
