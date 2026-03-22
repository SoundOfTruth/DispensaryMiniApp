type PaginationPage = number | "...";

export const calcPages = (
  start: number,
  end: number,
  pagesCount: number,
): PaginationPage[] => {
  const pages: PaginationPage[] = [1];

  if (start < 4) {
    start = 2;
  } else {
    pages.push("...");
  }
  if (pagesCount - end == 1) {
    end = pagesCount;
  }
  for (let i = start; i < end; i++) {
    pages.push(i);
  }
  if (end != pagesCount) {
    pages.push("...");
  }
  pages.push(pagesCount);
  return pages;
};
