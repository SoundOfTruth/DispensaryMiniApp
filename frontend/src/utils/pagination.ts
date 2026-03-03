export class Pagination {
  private size: number;
  private pagesCount: number;
  private pages: (number | null)[];

  constructor(pagesCount: number, size: number = 5) {
    this.size = size;
    this.pagesCount = pagesCount;
    this.pages = [];
  }

  private addOverflow(left: boolean, right: boolean): void {
    if (left && this.pages[0] && this.pages[1]) {
      const startDiff = this.pages[1] - this.pages[0];
      if (startDiff === 2) {
        this.pages.splice(1, 0, 2);
      } else if (startDiff !== 1) {
        this.pages.splice(1, 0, null);
      }
    }

    if (right) {
      const lastIndex = this.pages.length - 1;
      const endDiff = this.pagesCount - (this.pages[lastIndex] as number);
      if (endDiff === 2) {
        this.pages.push(this.pagesCount - 1);
      } else if (endDiff !== 1) {
        this.pages.push(null);
      }
    }
    if (this.pages[this.pages.length - 1] !== this.pagesCount) {
      this.pages.push(this.pagesCount);
    }
  }

  public getPages(currPage: number): (number | null)[] {
    this.pages = [1];

    const step = Math.floor(this.size / 2);

    if (currPage <= this.size - step) {
      if (this.pagesCount < this.size) {
        for (let i = 2; i <= this.pagesCount; i++) {
          this.pages.push(i);
        }
      } else {
        for (let i = 2; i < this.size; i++) {
          this.pages.push(i);
        }
        this.addOverflow(false, true);
      }
    } else if (this.pagesCount <= currPage + step) {
      for (let i = this.pagesCount - this.size + 2; i < this.pagesCount; i++) {
        this.pages.push(i);
      }
      this.addOverflow(true, false);
    } else {
      const adjustedStep = step - 1;
      const start = currPage - adjustedStep;
      const end = currPage + adjustedStep;

      for (let i = start; i <= end; i++) {
        this.pages.push(i);
      }
      this.addOverflow(true, true);
    }

    return this.pages;
  }
}
