class TestFile {
    public String foo() {
        return "bar";
    }

    private static void incorrectAssignmentInIfCondition() {
        boolean value = false;
        if (value = true) {
            //do Something
        } else {
            //else Do Something
        }
    }

    private static void incorrectComparingToItself() {
        int x = 342;
        if (x == x) {
            // whatever
        }
    }

    private static void anotherVariationOfIncorrectComparingToItself() {
        int x = 567;
        if (x <= x) {
            // whatever
        }
    }

    private static void onMoreVariationOfIncorrectComparingToItself() {
        int x = 23422;
        if (x*x == x*x) {
            // whatever
        }
    }
}
