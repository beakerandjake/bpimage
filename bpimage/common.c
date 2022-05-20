float clamp(float value)
{
    const float ret = value < 0 ? 0 : value;
    return ret > 255.0f ? 255.0f : ret;
}