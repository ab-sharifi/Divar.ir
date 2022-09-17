using System.ComponentModel.DataAnnotations;

namespace Divar.Data.Models
{
    public class HistoryLog
    {
        [Key]
        public int Id { get; set; }
        public int UserId { get; set; }
        public int PostId { get; set; }

        [Display(Name = "تاریخ بازدید")]
        [DataType(DataType.DateTime)]
        public DateTime LastVisit { get; set; }

        public virtual Users Users { get; set; }
        public virtual Posts Posts { get; set; }
    }
}
