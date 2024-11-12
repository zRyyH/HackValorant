#include <windows.h>
#include <stdio.h>

typedef struct
{
    int width;
    int height;
    unsigned char *data;
} CapturedImage;

CapturedImage captureScreen(int res_x, int res_y)
{
    int x = (res_x / 2) - 100;
    int y = (res_y / 2) - 20;
    int width = 200;
    int height = 40;

    HWND hDesktopWnd = GetDesktopWindow();
    HDC hDesktopDC = GetDC(hDesktopWnd);
    HDC hCaptureDC = CreateCompatibleDC(hDesktopDC);
    HBITMAP hCaptureBitmap = CreateCompatibleBitmap(hDesktopDC, width, height);
    SelectObject(hCaptureDC, hCaptureBitmap);

    BitBlt(hCaptureDC, 0, 0, width, height, hDesktopDC, x, y, SRCCOPY);

    ReleaseDC(hDesktopWnd, hDesktopDC);

    BITMAPINFOHEADER bi;
    bi.biSize = sizeof(BITMAPINFOHEADER);
    bi.biWidth = width;
    bi.biHeight = -height;
    bi.biPlanes = 1;
    bi.biBitCount = 24;
    bi.biCompression = BI_RGB;
    bi.biSizeImage = 0;

    CapturedImage capturedImage;
    capturedImage.width = width;
    capturedImage.height = height;

    int bytesPerPixel = 3;
    int padding = (4 - (width * bytesPerPixel) % 4) % 4;

    capturedImage.data = (unsigned char *)malloc((width * bytesPerPixel + padding) * height);
    GetDIBits(hCaptureDC, hCaptureBitmap, 0, height, capturedImage.data, (BITMAPINFO *)&bi, DIB_RGB_COLORS);

    DeleteObject(hCaptureBitmap);
    DeleteDC(hCaptureDC);

    return capturedImage;
}

void freeCapturedImage(CapturedImage *capturedImage)
{
    free(capturedImage->data);
}

int main(int res_x, int res_y)
{
    CapturedImage capturedImage = captureScreen(res_x, res_y);
    freeCapturedImage(&capturedImage);
    return 0;
}
