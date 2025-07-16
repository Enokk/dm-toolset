import { definePreset } from '@primeuix/themes'
import Aura from '@primeuix/themes/aura'

export default definePreset(Aura, {
    semantic: {
        primary: {
            50: '{cyan.50}',
            100: '{cyan.100}',
            200: '{cyan.200}',
            300: '{cyan.300}',
            400: '{cyan.400}',
            500: '{cyan.500}',
            600: '{cyan.600}',
            700: '{cyan.700}',
            800: '{cyan.800}',
            900: '{cyan.900}',
            950: '{cyan.950}'
        },
        secondary: {
            50: '{fuchsia.50}',
            100: '{fuchsia.100}',
            200: '{fuchsia.200}',
            300: '{fuchsia.300}',
            400: '{fuchsia.400}',
            500: '{fuchsia.500}',
            600: '{fuchsia.600}',
            700: '{fuchsia.700}',
            800: '{fuchsia.800}',
            900: '{fuchsia.900}',
            950: '{fuchsia.950}'
        },
        colorScheme: {
            light: {
                primary: {
                    color: '{cyan.950}',
                    inverseColor: '#ffffff',
                    hoverColor: '{cyan.900}',
                    activeColor: '{cyan.800}',
                },
                secondary: {
                    color: '{fuchsia.700}',
                    inverseColor: '#ffffff',
                    hoverColor: '{fuchsia.900}',
                    activeColor: '{fuchsia.800}'
                },
                highlight: {
                    background: '{cyan.950}',
                    focusBackground: '{cyan.700}',
                    color: '#ffffff',
                    focusColor: '#ffffff'
                }
            },
        }
    }
  });