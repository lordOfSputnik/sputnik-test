class TestFile {
    public String foo() {
        return "bar";
    }

    private static void incorrectAssignmentInIfCondition() {
        boolean value = false;
        if (value = false) {
            //do Something
        } else {
            //else Do Something
        }
    }

    private static void incorrectComparingToItself() {
        int x = 3421;
        if (x <= x) {
            // whatever
        }
    }

    private static void anotherVariationOfIncorrectComparingToItself() {
        int x = 999;
        if (x == x) {
            // whatever
        }
    }

    private static void onMoreVariationOfIncorrectComparingToItself() {
        int x = 8888;
        if (x <= x) {
            // whatever
        }
    }
}
