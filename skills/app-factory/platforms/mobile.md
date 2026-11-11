# Platform: mobile

Read when `plan.md` says the platform is mobile or both.

**Technology options to compare (stage 1):** native iOS (Swift) and native Android (Kotlin), Flutter, React Native, or another fit. Compare on performance, access to device features the app needs, one codebase versus two, development speed and maintenance. Ask which phones matter (iOS, Android or both) and the oldest OS version to support.

**Design (stage 2):** follow each platform's conventions for navigation and controls; touch targets of at least 44 pt (iOS) or 48 dp (Android); small and large phones, and tablets if in scope; safe areas, dark mode, system text sizes.

**Build plan (stage 3):** signing and bundle identifiers, store accounts, and build distribution (TestFlight, Play testing tracks) are tasks. Building for iOS needs a Mac with Xcode.

**QA (stage 5):** iOS simulators and Android emulators for the supported OS versions and screen sizes. Real devices only if the user provides them or approves a device-farm service. State what was covered. Check camera, notifications, offline use and other device features the app relies on.

**Security review:** local storage of sensitive data, transport security settings, what the built app exposes.

**Launch (stage 6):** App Store and Google Play listing text and screenshot plan within current store limits; store review rules that apply (privacy labels, purchases, sign-in); developer accounts and their fees; a first submission is manual and needs the user.
