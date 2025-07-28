import { definePreset } from '@primeuix/themes'
import Aura from '@primeuix/themes/aura'

export default definePreset(Aura, {
    semantic: {
        primary: {
            50: '#f0f9ff',
            100: '#e0f2fe',
            200: '#bae6fd',
            300: '#7dd3fc',
            400: '#38bdf8',
            500: '#0ea5e9',
            600: '#0284c7',
            700: '#0369a1',
            800: '#075985',
            900: '#0c4a6e', 
            950: '#082f49'
        },
        colorScheme: {
            dark: {
                surface: { 
                    0: '#ffffff',
                    50: '#f4f4f4',
                    100: '#e8e9e9',
                    200: '#d2d2d4',
                    300: '#bbbcbe',
                    400: '#a5a5a9',
                    500: '#8e8f93',
                    600: '#77787d',
                    700: '#616268',
                    800: '#4a4b52',
                    900: '#34343d',
                    950: '#1d1e27' 
                },
                text: {
                    color: '{surface.100}',
                    mutedColor: '{surface.300}',
                },
                primary: {
                    color: '{primary.400}',
                    contrastColor: '{surface.950}',
                    hoverColor: '{primary.300}',
                    activeColor: '{primary.200}' // TODO: check if this is right
                },
                content: {
                    background: '{surface.900}',
                }
            }
        }
    }
  });